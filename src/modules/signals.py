import numpy as np
from copy import copy
import sympy
from scipy import interpolate as interp
from modules.utility import print_debug, print_log


class Signal():
    """Represents a signal"""

    def __init__(self, magnitude=[], fsample=0, time=[], coef=[]) -> None:

        self.magnitude = magnitude
        self.fsample = fsample
        self.time = time

        if self.fsample == 0:
            self.time = time
            if len(time) != 0:
                self.fsample = len(self.magnitude)/time[-1]

        if len(time) == 0:
            if len(magnitude) != 0:
                print_debug("Time axis auto generated")
                self.time = np.arange(0, len(magnitude))/fsample
            else:
                self.time = []

        # if (self.magnitude != [] and self.time == []) or (self.magnitude == [] and self.time != []):
        #     raise Exception("Signal must have a time or fsampling vector")

        self.coefficients = coef

    def __len__(self):
        """Returns the length of the signal"""
        if self.magnitude != []:
            return len(self.magnitude)
        else:
            print_debug("Signal has 0 length")
            return 0

    def __getitem__(self, index):
        """Returns the signal at the given index"""
        return copy(Signal(self.magnitude[index], self.fsample, self.time[index]))

    def __add__(self, other):
        """Adds two signals"""
        if self.fsample == other.fsample:
            return Signal(self.magnitude + other.magnitude, self.fsample, self.time)
        else:
            raise Exception("Signals must have the same sampling frequency")

    def __subtract__(self, other):
        """Subtracts two signals"""
        if self.fsample == other.fsample:
            return Signal(self.magnitude - other.magnitude, self.fsample, self.time)
        else:
            raise Exception("Signals must have the same sampling frequency")

    def set_max_samples(self, max_samples):
        """Sets the maximum number of samples"""
        if len(self.magnitude) > max_samples:
            self.magnitude = self.magnitude[:max_samples]
            self.time = self.time[:max_samples]

    def __append__(self, other):
        """Appends two signals"""
        if self.fsample == other.fsample:
            return copy(Signal(self.magnitude + other.magnitude, self.fsample, self.time + other.time))
        else:
            raise Exception("Signals must have the same sampling frequency")

    def clip(self, direction, percentage):
        """Clips the signal"""
        percentage = percentage / 100
        if direction == "left":
            self.magnitude = self.magnitude[int(
                len(self.magnitude) * (1 - percentage)):]
            self.time = self.time[int(len(self.time) * (1 - percentage)):]
        elif direction == "right":
            self.magnitude = self.magnitude[:int(
                len(self.magnitude) * (1 - percentage))]
            self.time = self.time[:int(len(self.time) * (1 - percentage))]
        else:
            raise Exception("Direction must be left or right")

    def set_data(self, magnitude, time):
        """Sets the magnitdue and time of the signal"""
        self.magnitude = magnitude
        self.time = time
        if len(self.magnitude) != len(self.time):
            raise Exception("Signal must have the same length")
        if len(self.magnitude) != 0:
            self.fsample = len(self.magnitude)/time[-1]

    def set_coefficients(self, coef):
        self.coefficients = coef

    def get_coefficients(self):
        return self.coefficients


class ChunkedSignal(Signal):
    """Represents a chunked signal"""

    def __init__(self, signal, max_chunks: int = 0, overlap_percent: int = 0) -> None:
        super().__init__(signal.magnitude, signal.fsample, signal.time)

        self.chunk_array = []
        """Array of full chunk signal objects (includes overlap)"""
        self.chunk_length = 0
        self.overlap_percent = overlap_percent
        if len(signal.magnitude) > 0:
            self.update_chunk_size(max_chunks)
            # self.generate_chunks()

    def update_chunk_size(self, max_chunks):
        if max_chunks == 0:
            max_chunks = 1
        self.chunk_length = round(len(self.magnitude)/max_chunks)
        print_debug("Chunk length: " + str(self.chunk_length))
        print_debug("Overlap percent: " + str(self.overlap_percent))
        self.overlap_length = int(np.ceil(
            self.chunk_length * (self.overlap_percent/100)))  # TODO: FIX THIS
        self.generate_chunks()

    def merge_chunks(self):
        """Merges chunks into the main signal superclass"""

        # clear data
        self.time = []
        self.magnitude = []

        for index in range(0, len(self.chunk_array)):
            print_debug("Merging chunk " + str(index))
            print_debug(self.chunk_array[index])
            # for each chunk

            averaged_overlap = []
            overwritten_chunk = []
            remaining_chunk = []

            # average the chunk+overlap and add to main signal
            if index == len(self.chunk_array) - 1:
                averaged_overlap = []  # last chunk cornercase
            elif index == 0:
                averaged_overlap = self.get_overlap_magnitudes(
                    index, "left")
            else:
                averaged_overlap = self.average_overlap(index)

            # overwrite the left side overlap of the next chunk
            # append the left averaged overlap to actual chunk

            remaining_chunk = self.get_chunk_without_overlap(
                index).magnitude[self.overlap_length:self.chunk_length]  # chunk starting after left overlap
            print_debug("Remaining chunk: " + str(remaining_chunk))

            overwritten_chunk = np.concatenate(
                (averaged_overlap, remaining_chunk), axis=None)

            print_debug("Overwritten Chunk: " + str(overwritten_chunk))
            # add to main signal

            appended_time = self.get_chunk_without_overlap(index).time

            if len(appended_time) != len(overwritten_chunk):
                difference = len(appended_time) - len(overwritten_chunk)
                print_debug("Target Length: " + str(len(appended_time)))
                print_debug("Length before padding: " +
                            str(len(overwritten_chunk)))
                overwritten_chunk.resize(len(appended_time))
                print_debug("Length after padding: " +
                            str(len(overwritten_chunk)))

            self.time.append(appended_time)
            self.magnitude.append(overwritten_chunk)

        # Convert to 1D arrays
        self.time = np.concatenate(self.time)
        self.magnitude = np.concatenate(self.magnitude)

    def average_overlap(self, chunk_index):
        """Averages the overlap magnitude of two chunks"""
        # get the overlap of left chunk and right chunk
        right_chunk_overlap = self.get_overlap_magnitudes(
            chunk_index, "left")
        left_chunk_overlap = self.get_overlap_magnitudes(
            chunk_index-1, "right")

        print_debug("Right chunk overlap: " + str(right_chunk_overlap))
        print_debug("Left chunk overlap: " + str(left_chunk_overlap))

        # average the overlap
        average_overlap = np.mean(
            [left_chunk_overlap, right_chunk_overlap], axis=0)

        print_debug("Average overlap: " + str(average_overlap))
        # return the averaged overlap (make sure to put it in the right chunk)
        return average_overlap

    def get_overlap_magnitudes(self, chunk_index, direction="right"):
        """Returns the overlap of the chunk from the given
        \n chunk index = index of chunk to get overlap from
        \n direction = location of overlap wrt to current chunk
        \n (accounts for leftmost and rightmost cornercases)
        \n returns a magnitude array """
        overlap_length = self.overlap_length
        print_debug("Overlap length: " + str(overlap_length))
        chunk_length = self.chunk_length
        print_debug("Chunk length: " + str(chunk_length))

        if direction == "left":
            print_debug("Getting left overlap")
            return self.chunk_array[chunk_index][:overlap_length].magnitude
        elif direction == "right":
            if chunk_index != len(self.chunk_array)-1:
                print_debug("Getting right overlap")
                return self.chunk_array[chunk_index][chunk_length:chunk_length+overlap_length].magnitude
            else:
                if overlap_length != 0:
                    overlap_length -= 1
                return np.zeros(overlap_length)  # Zero padding
        else:
            raise Exception("Direction must be left or right")

    def get_chunk(self, index):
        """Returns the chunk at the given index"""
        return self.chunk_array[index]

    def get_chunk_without_overlap(self, index):
        """Returns the chunk signal object without overlap"""
        output = copy(self.chunk_array[index][:self.chunk_length])
        print_debug(" Chunk without overlap" + str(output))
        return output

    def get_coefficients(self, index=0):
        """Returns the coefficients of the chunk at the given index"""
        return self.chunk_array[index].coefficients

    def set_chunk(self, chunk_index, signal):
        """Modifies a single chunk signal"""
        # TODO: add corner case
        # add signal object to chunk
        self.chunk_array[chunk_index] = signal
        # call update merged chunks
        self.merge_chunks()

    def generate_chunks(self):
        """Generates signal objects for each chunk + overlap"""

        # generate chunks
        chunk_array = []
        chunk_length = self.chunk_length
        overlap_length = self.overlap_length

        for index in range(0, len(self.magnitude), chunk_length):
            chunk_array.append(Signal(self.magnitude[index:index+chunk_length + overlap_length],
                                      self.fsample,
                                      self.time[index:index +
                                                chunk_length + overlap_length],
                                      self.coefficients))

        self.chunk_array = chunk_array
