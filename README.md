# CodeValidator
With a button click checks the code and sends feedback to student email


CodeValidator
This application is implemented with python on Web2py framework
In this application Teacher can submit the problems and Student can submit the solutions to them. The main purpose of this application is instead of running the student programs manually and sending email manually, with a button click it will run the student submission and send a mail to the student. The problems/Assignments can be any of C, Java or Python programs. 
Features:
1.	Teacher will be provided with a button to create assignments.  For each of the assignment teacher has to provide the Due Date. So if the due date is finished, in the student it will show a message to student and will not allow the student to submit the solution.
2.	Teacher can edit or delete the assignments whenever he wants.
3.	When the teacher creates assignment he has to describe format of the input file she is going to test with and also about how the output should look like. (The student programs should accept a file as a parameter)
4.	Teacher can also provide an image related to the problem. So in student page we will show it as a thumbnail and if the student clicks on it will popped up.
5.	Teacher has to provide the ‘Test input file’ and ‘Test output file’ to check the submissions. These will not be shown to the students.
6.	In teacher page it will be shown with all the Assignments/Problems titles that have been created so far and Total number of solutions for each of them. If the teacher clicks on Title of a problem he can see the description, thumbnail of image and student email ids who all have submitted the solutions for that problem. Teacher can download and see their submissions as well.
7.	Student page looks similar to the teacher page except the button to create an assignment.  If the student clicks on the title of the assignment he can see the description, thumbnail and a form to provide solution.
8.	We are validating the form such a way that for each problem student can submit the solution only once.
9.	While creating the assignment it will allow the teacher to select Type of the assignment as Immediate feedback or Not Immediate feedback. If the assignment is of Immediate then once the student submits the solution, he/she will get the feedback to the provided email. If it is of Not Immediate feedback then Teacher will be provided with a ‘Compile’ button for those submissions. Once the teacher clicks on ‘Compile’ button he can see whether the submission is correct or incorrect and also an automatic mail will be sent to the student.


Problems:
The main problem with this application is security. The student might submit any hazardous file.
Also the student submission might have an infinite loop and we did not implement any logic to kill them after certain time, if the program is running for long time.
Also since the application do not need to have SignUp for the student,  a student can submit solutions with others email id.
One more problem is, the student may submit incorrect files. For example if the teacher is asking for Java program the student may implement same logic in C or Python and submit it. This application do not have any such validation.
