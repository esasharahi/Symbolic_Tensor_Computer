#!/usr/bin/env python
## esasharahi@gmail.com
# Filename: ece.py

## Needed Modules
import re # For almost all functions
import string # For dummy_killer function
##

## Functions
def dummy_killer(in_ten):
	'''
	This function, acts on a single tensor without any multiplication by another tensor or any summation of some tensors. 
	The general input for this function is such "2*f*g*A^{blala}_{blala}". 
	It is ready to kill dummy summation indices in two different classes. We illastrated these classes by capital and small
	English alphabet numbers. So, e.g "3*f*h*A^{s fA}_{fh}" is completely legal for dummy_killer function.
	Indeed, the domain of its acts is only the "^{s fA}_{fh}" and so the  "3*f*h*A" part is safe and not acted.
	Thus, do not worry about using a letter (never mind to be capital or small) 
	as an index and function or tensor name at the same time.   
	'''
## Specifying summation indices
	sums_ones = set(detailed_tensor(in_ten)[-2]) & set(detailed_tensor(in_ten)[-1])
	SumIndices = sorted([x for x in sums_ones if x != ' '])
## Specifying single indices
	single_ones = set(detailed_tensor(in_ten)[-2]) ^ set(detailed_tensor(in_ten)[-1])
	SingleIndices = sorted([x for x in single_ones if x != ' '])
## Killing dummy ones 
	AlphabeticalList = list(string.ascii_uppercase) + list(string.ascii_lowercase)
	ModifiedAlphabeticalList = [x for x in AlphabeticalList if x not in SingleIndices]
	CapitalSumIndices = [x for x in SumIndices if x in list(string.ascii_uppercase)]
	SmallSumIndices = [x for x in SumIndices if x in list(string.ascii_lowercase)]
	CapitalModifiedAlphabeticalList = [x for x in ModifiedAlphabeticalList if x in list(string.ascii_uppercase)]
	SmallModifiedAlphabeticalList = [x for x in ModifiedAlphabeticalList if x in list(string.ascii_lowercase)]
## Making dummyless sum indices
	CapitalFinal = CapitalModifiedAlphabeticalList[0:len(CapitalSumIndices)]
	SmallFinal = SmallModifiedAlphabeticalList[0:len(SmallSumIndices)]
	Final = CapitalFinal + SmallFinal
## Substitute dummylesses with dummies
	ready_for_sub = zip(SumIndices, Final)
	target_for_change = in_ten[in_ten.find("^{")+2:]
	old_target_for_change = target_for_change
	for old, new in ready_for_sub:
		target_for_change = target_for_change.replace(old, new)
#	print(new_target_for_change)
	in_ten = in_ten.replace(old_target_for_change, target_for_change)
	return(in_ten)
### End dummy_killer function
def detailed_tensor(tensor):
	'''
	The tensor must be something like "A^{blabla}_{blabla}".
	If you want to split a tensor with a summation, 
	use the function "tensor_splitter". 
	Tensor_dimension is a list [n, m] that shows that a pure tensor 
	is n times covariant and m times contravariant.
	The output is a 4-list:
	[input, [list of input coefficients], [modified list of input coefficient], tensor name, 
	[n, m], [list of superscripts], [list of subscripts]].
	'''
## Manipulate tensor structure
	tensor_name_finder = re.match(r"(.*)\^{", tensor)
	tensor_name = "_"+tensor_name_finder.group(1)
	superscripts = tensor[tensor.find("^{")+2:tensor.find("}_")]
	pre_subscripts = tensor[tensor.find("_{")+2:]
	subscripts = pre_subscripts[:-1]
## Making list of data
	pre_coefs = list(tensor_name_finder.group(1))
	pure_tensor_name = pre_coefs[-1]
	del pre_coefs[-1]
	tensor_name_list = []
	tensor_name_list.append(tensor)
	tensor_name_list.append(pre_coefs)
	tensor_name_list.append("niced_coefs")
	tensor_name_list.append(pure_tensor_name)
	tensor_dimension = [len(superscripts), len(subscripts)]
	tensor_name_list.append(tensor_dimension)
	tensor_name_list.append(list(superscripts))
	tensor_name_list.append(list(subscripts))
	return(tensor_name_list)
	#return(tensor_name_finder.group(1))
### End detailed_tensor function
def tensor_splitter(tensor): 
	'''
	This function, splits a summation of tensors using "detailed_tensor" function.
	'''
	splited_tensor = re.split("\+", tensor.replace("-", "+-"))
	if splited_tensor[0:1] == ['']:
		del splited_tensor[0:1]
	print(splited_tensor)
	for i in splited_tensor:
		print(detailed_tensor(i))
### End tensor_splitter function
def tensor_filter(tensor):
	'''
	This function acts on a SINGLE tensor and decompose it into three slices:
	1) The sign of the tensor
	2) The coefficients in the tensor
	2) The pure tensor
	Do not forget that you SHOULD use * for any multiplication. 
	'''
	filtered_tensor = []
	if tensor[:1] == "-":
		tensor_sign = "-"
		tensor = tensor[1:]
		tensor = "*" + tensor
		all_tensor = re.match(r"(.*)()([A-Za-z]\^.*)", tensor)
		tensor_pure = all_tensor.group(3)
		pre_tensor_coef = all_tensor.group(1)
		str_tensor_coef = pre_tensor_coef
		tensor_coef = str(str_tensor_coef)
		tensor_coef = tensor_coef.replace("*", " ")
		tensor_coef = tensor_coef[:-1]
		tensor_coef = tensor_coef[1:]
		
		tensor_coef = tensor_coef.split()
	else:
		tensor_sign = "+"
		tensor = "*" + tensor
		all_tensor = re.match(r"(.*)()([A-Za-z]\^.*)", tensor)
		tensor_pure = all_tensor.group(3)
		pre_tensor_coef = all_tensor.group(1)
		str_tensor_coef = pre_tensor_coef
		tensor_coef = str(str_tensor_coef)
		tensor_coef = tensor_coef.replace("*", " ")
		tensor_coef = tensor_coef[:-1]
		tensor_coef = tensor_coef[1:]
	filtered_tensor.append(tensor_sign)
	filtered_tensor.append(tensor_coef)
	filtered_tensor.append(tensor_pure)
	if [] in filtered_tensor:
		del filtered_tensor[1]
	coefs = filtered_tensor[1]
	all_numbers = [r for r in coefs if r.isdigit()]
	finall_number = 1
	for i in all_numbers:
		finall_number = finall_number * float(i)
	coefs = [i for i in coefs if re.match(r'[A-Za-z]', i)]
	coefs = [str(finall_number)] + coefs
	filtered_tensor[1] = coefs
	return(filtered_tensor)
## End of tensor_filter function

def simple_sum(tensor1, tensor2):
	'''
	This function takes two single tensor and sum them.
	'''
	ten1 = tensor_filter(tensor1)
	ten2 = tensor_filter(tensor2)
	if ten1[2] == ten2[2]:
		if ten1[1] == ten2[1]:
			if ten1[0] == ten2[0]:
				pre_simple_sum = "2*" + tensor1
				main_simple_sum = re.sub(r"(2).*(-)","-2*", pre_simple_sum)
				return main_simple_sum
			else:
				return(0)
		elif ten1[0] != ten2[0]:
				pre_simple_sum = tensor1 + " + " + tensor2
				main_simple_sum = re.sub(r"(\+).*(-)","-", pre_simple_sum)
				return main_simple_sum
	else: 
		pre_simple_sum = tensor1 + " + " + tensor2
		main_simple_sum = re.sub(r"(\+).*(-)","-", pre_simple_sum)
		return main_simple_sum
## End of simple_sum function


# End of ece.py
