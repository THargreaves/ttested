"""A Python module for visualising various sorting algorithms.

The following sorting algorithms are implemented at present:
    * Bubble Sort
    * Selection Sort
    * Insertion Sort
    * Cocktail Sort

The rules for the visualisations are as follows:
    * We have an array of length n to be sorted
    * The elements of the array are the integers 0 to n-1
    * If a[i]=v then we say that the point with value v is in position i
    * Each point in the visualisation represents an array element
    * The colour of each point is determined by this element's value
    * Likewise a point's rotational position is based on its value
    * The radial position of a given point at a certain step in a sort
      (or shuffle) is determined by the modulus of the absolute
      difference between its position and value
    * In other words, this is the minimal cyclical distance between
      where the element is and where it should be

You can tweak parameters of the animation at the start of the abstract
class definition. Have fun!
"""

# imports
import colorsys as col
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import random as rnd

from abc import ABC, abstractmethod


class SortingAnimation(ABC):
    """Abstract class for generic sorting animations."""

    # class parameters
    num_points = 720  # should be a multiple of two
    point_size = 6
    pre_shuffle_pause = 30  # in frames at 60fps
    post_shuffle_pause = 60  # likewise
    shuffle_speed = 4  # should evenly divide num_points

    def __init__(self):
        """Create array to sort, colour palette, and initial plot."""
        # array to sort
        self.arr = np.arange(self.num_points)

        # colour palette
        self.cols = [col.hsv_to_rgb(i / self.num_points, 1, 0.8)
                     for i in range(self.num_points)]

        # store normalised x,y coordinates to speed up animation
        self.x_norm = np.sin(np.arange(self.num_points) /
                             self.num_points * (2 * np.pi))
        self.y_norm = np.cos(np.arange(self.num_points) /
                             self.num_points * (2 * np.pi))

        # create plot
        self.fig = plt.figure()
        self.fig.set_size_inches(6, 6)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        self.ax.set_axis_off()
        self.fig.add_axes(self.ax)
        self.scat = self.ax.scatter(self.x_norm, self.y_norm,
                                    color=self.cols, s=self.point_size)

        # default file name, overrided in child __init__() method
        if not hasattr(self, 'file_name'):
            self.file_name = 'sort.mp4'

        super().__init__()

    def swap_elements(self, i, j):
        """Swap two elements in the instance array."""
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def write_animation(self):
        """Output animation to MP4 file."""
        # create animation driver
        sort_anim = anim.FuncAnimation(
            self.fig,
            self.animate,
            interval=1000 / 30,
            frames=self.pre_shuffle_pause + self.num_points +
            self.num_points // self.shuffle_speed +
            self.post_shuffle_pause
        )

        # output animation
        print('Beginning Animation Process')
        writer = anim.writers['ffmpeg'](fps=60, bitrate=1800)
        sort_anim.save(self.file_name, writer=writer,
                       savefig_kwargs={'facecolor': 'black'})
        print('Animation Saved')

    @abstractmethod
    def sort_step(self, step_num):
        """Sort the array. Abstract method to be overrided."""
        pass

    def shuffle_step(self, frame_num):
        """Shuffle the array using the Fisher-Yates algorithm."""
        for step_num in range(frame_num * self.shuffle_speed,
                              (frame_num + 1) * self.shuffle_speed):
            # no change needed to be made on first step
            if step_num == 0:
                continue

            # pick a random element from non-shuffled elements
            j = rnd.randint(step_num, self.num_points - 1)
            self.swap_elements(step_num-1, j)
        self.update_coords()

    def animate(self, frame_num):
        """Animate the next frame of the animation."""
        if frame_num < self.pre_shuffle_pause:
            return
        elif frame_num < self.pre_shuffle_pause + \
                self.num_points // self.shuffle_speed:
            self.shuffle_step(frame_num - self.pre_shuffle_pause)
        elif frame_num < self.pre_shuffle_pause + \
                self.num_points // self.shuffle_speed + \
                self.post_shuffle_pause:
            return
        else:
            self.sort_step(frame_num - (self.pre_shuffle_pause +
                           self.num_points // self.shuffle_speed +
                           self.post_shuffle_pause))
        if frame_num % 100 == 0:
            print('Animating frame', frame_num)

    def update_coords(self):
        """Update point coordinates from array positions."""
        # compute differences
        diff = np.minimum(
            np.mod(
                self.arr - np.arange(self.num_points),
                np.full(self.num_points, self.num_points)
            ), np.mod(
                np.arange(self.num_points) - self.arr,
                np.full(self.num_points, self.num_points))
            )

        # compute coordinates
        x = (1 - diff / self.num_points * 2) * self.x_norm
        y = (1 - diff / self.num_points * 2) * self.y_norm

        # update plot
        self.scat.set_offsets(np.c_[x, y])


class BubbleSortAnimation(SortingAnimation):
    """A class for animating the bubble sort."""

    def __init__(self):
        """Override default file name and call parent init method."""
        # override file name
        self.file_name = 'bubble.mp4'

        super().__init__()

    def sort_step(self, step_num):
        """Sort the array. Overrides abstract method of parent."""
        for j in range(self.num_points - step_num - 1):
            if self.arr[j] > self.arr[j + 1]:
                self.swap_elements(j, j + 1)
        self.update_coords()


class SelectionSortAnimation(SortingAnimation):
    """A class for animating the selection sort."""

    def __init__(self):
        """Override default file name and call parent init method."""
        # override file name
        self.file_name = 'selection.mp4'

        super().__init__()

    def sort_step(self, step_num):
        """Sort the array. Overrides abstract method of parent."""
        min_index = step_num
        for j in range(step_num + 1, self.num_points):
            if self.arr[min_index] > self.arr[j]:
                min_index = j
        self.swap_elements(step_num, min_index)
        self.update_coords()


class InsertionSortAnimation(SortingAnimation):
    """A class for animating the insertion sort."""

    def __init__(self):
        """Override default file name and call parent init method."""
        # override file name
        self.file_name = 'insertion.mp4'

        super().__init__()

    def sort_step(self, step_num):
        """Sort the array. Overrides abstract method of parent."""
        # nothing needs to be done on first iteration
        if step_num == 0:
            return

        key = self.arr[step_num]
        j = step_num-1

        while j >= 0 and key < self.arr[j]:
            self.arr[j + 1] = self.arr[j]
            j -= 1
        self.arr[j + 1] = key

        self.update_coords()


class CocktailSortAnimation(SortingAnimation):
    """A class for animating the cocktail sort."""

    def __init__(self):
        """Override default file name and call parent init method."""
        # override file name
        self.file_name = 'cocktail.mp4'

        super().__init__()

    def sort_step(self, step_num):
        """Sort the array. Overrides abstract method of parent."""
        if step_num % 2 == 0:
            for j in range(step_num // 2,
                           (self.num_points - 1) - step_num // 2):
                if self.arr[j] > self.arr[j + 1]:
                    self.swap_elements(j, j + 1)
        else:
            for j in range((self.num_points - 1) - (step_num + 1) // 2,
                           (step_num - 3) // 2, -1):
                if self.arr[j] > self.arr[j + 1]:
                    self.swap_elements(j, j + 1)

        self.update_coords()


# driver code
if __name__ == '__main__':
    print('Creating Bubble Sort Animation')
    bubble = BubbleSortAnimation()
    bubble.write_animation()

    print('Creating Selection Sort Animation')
    selection = SelectionSortAnimation()
    selection.write_animation()

    print('Creating Insertion Sort Animation')
    insertion = InsertionSortAnimation()
    insertion.write_animation()

    print('Creating Cocktail Sort Animation')
    cocktail = CocktailSortAnimation()
    cocktail.write_animation()
