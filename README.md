# cisc-121-final-project
Final project for CISC121
Recording: 

https://github.com/user-attachments/assets/c410f30d-cbc8-4468-9c1e-1c0840b04faf


## Algorithm chosen: Insertion sort

I chose insertion sort because it can be used in complex scenarios where merge sort and quick sort cannot be applied. Insertion sort triumphs over these other sorting algorithms when the scenario involves small datasets. In addition, insertion sort is the fastest for nearly sorted datasets as well. 

This is insertion sort step-by-step:
Start at the second element
Compare if current element, i, is smaller than i-1
If current element, i, is smaller than swap with i-1
Move to the next element and do the same comparisons
if no if statements hold true, move to next element

## Decomposition:

Get user input: an unsorted list of numbers
Check if input is correct
Start with first element
Store numbers into array 
Track each step and use a diagram to show the sort live
Return final sorted array

## Pattern Recognition:

Each iteration inserts an element into its correct position. This causes the list to shift right until the element is sorted properly. The current element is always compared with the element from behind.

## Algorithm design

Input → Processing → Output flow:

Input: Textbox for comma-separated integers, YES/NO buttons for each comparison decision
Processing: Insertion sort logic tracks temp, hole, and i across passes; each user answer either shifts a neighbour right or places temp at the hole; final pass validates whether the result is genuinely sorted
Output:

Bar chart visualization of the full array, coloured by role (sorted, inserting, comparing, unsorted, complete)
Status textbox showing the current comparison question or final result message
Step log recording every shift, placement, and pass decision in order


GUI: Buttons for "Start Sorting", "YES — Swap", "NO — Keep", "Reset"

## Problem breakdown

When sorting a close to sorted list or a small list, other algorithms can take longer to sort. This is why insertion sort was created to sort these datasets faster and more efficiently. For me, insertion sort was hard for me to visualize, so I chose to create this visualizer to help demonstrate how insertion sort works.

## Design 

The program is meant to teach the user how insertion sort works. It demonstrates this by using bars assigned to numeric values and shows what each iteration does. The program gives the user two options, yes or no, to whether the program should swap the bars that are being compared.

## Testing 

## An unsorted valid array:
<img width="404" height="700" alt="image" src="https://github.com/user-attachments/assets/8b9c2670-a310-4f1b-b419-1e19c350b412" />

## A sorted array:
<img width="547" height="830" alt="image" src="https://github.com/user-attachments/assets/0383db50-ea56-46d0-95af-bc8af66b90bd" />

## A reverse sorted array:
<img width="405" height="691" alt="image" src="https://github.com/user-attachments/assets/b92e3e3a-6d79-438e-ab67-1ba090049da5" />

## An array with duplicate values:
<img width="532" height="830" alt="image" src="https://github.com/user-attachments/assets/8aec907d-9ada-4fb1-a3ff-049d0c728ab5" />

## An array with only duplicate values:
<img width="551" height="834" alt="image" src="https://github.com/user-attachments/assets/285bb80f-9b51-46c9-b7f8-0f6f7149e297" />


## How to run

Clone repository and install gradio using pip with: pip install gradio
Then run python app.py

Alternatively, use the hugging face link:
https://huggingface.co/spaces/Wizzzdo/Visualizing_Insertion_sort




