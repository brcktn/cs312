class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        used = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in used:
                return [used[diff], i]
            used[num] = i