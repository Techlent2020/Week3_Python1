Homework week1
Leetcode NO.
167
219
242
268
349
350
389
442
448
575



Solutions:

leetcode 167
class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        #build the lookup hashmap, 
        pair = {}
        for i,v in enumerate(numbers):
            pair[v] = i
        #start to look of elements
        for i in range(len(numbers)):
            if target-numbers[i] in pair:
                tarI = pair[target-numbers[i]]
                # in the case i == tarI, logically, you need to add the following two lines of code.
                # but with or without the following two lines of code, it returns the right results. Think about why it is.
                #if i == tarI:
                    #continue
                if i > tarI:
                    return [tarI+1, i+1]
                else:
                    return [i+1, tarI+1]

leetcode 219

class Solution(object):
    def containsNearbyDuplicate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """
        if len(nums) < 1:
            return False
        hashmap = {}
        for index, value in enumerate(nums):
            if value not in hashmap:
                hashmap[value] = index
            else:
                if abs(index-hashmap[value]) <= k:
                    return True
                else:
                	#if the value is in hashmap, we still need to update the index since we want the index difference as small as possible.
                    hashmap[value] = index
                    continue
        return False

leetcode 242
class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        hashmap = {}
        for e in s:
            if e not in hashmap:
                hashmap[e] = 1
            else:
                hashmap[e] += 1
        for e in t:
            if e not in hashmap:
                return False
            hashmap[e] -= 1
        for key in hashmap:
            if hashmap[key] != 0:
                return False
        return True

leetcode 268

class Solution(object):
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        s = set(nums)
        for i in range(len(nums) + 1):
            if i not in s:
                return i

leetcode 349

class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        set1 = {e for e in nums1}
        set2 = {e for e in nums2}
        return list(set1&set2)

leetcode 350

class Solution(object):
    def intersect(self, nums1, nums2):

        counts = {}
        res = []

        #Another way to initiallize a dictionary. If you are not comfortable to use it in this way, just do it as we tought in the class.
        for num in nums1:
            counts[num] = counts.get(num, 0) + 1

        for num in nums2:
            if num in counts and counts[num] > 0:
                res.append(num)
                counts[num] -= 1

        return res

leetcode 389

class Solution(object):
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        dict_t = {}
        for x in s:
            if x not in dict_t:
                dict_t[x] = 1
            else:
                dict_t[x] +=1
        for y in t:
            if y not in dict_t:
                return y
            else:
                dict_t[y] -=1
                if dict_t[y] == -1:
                    return y

leetcode 442

class Solution(object):
    def findDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        if not nums:
            return []
        #rL is the return list
        rL = []
        # initiallize the dictionary
        hashmap = {}
        for e in nums:
            if e not in hashmap:
                hashmap[e] = 1
            else:
                hashmap[e] += 1
                if hashmap[e] == 2:
                    rL.append(e)
        return rL

leetcode 448

class Solution(object):
    def findDisappearedNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        hashmap = {}
        for e in nums:
            if e not in hashmap:
                hashmap[e] = 1
            else:
                hashmap[e] += 1
        
        res = []
        for i in range(1, len(nums) + 1):
            if i not in hashmap:
                res.append(i)
        return res

leetcode 575

class Solution(object):
    def distributeCandies(self, candies):
        """
        :type candies: List[int]
        :rtype: int
        """
        num = len(candies)/2
        kinds = len(set(candies))
        return min(num, kinds)
