function calculateAverage(grades)
{
let sum = 0;
for (i = 0; i < grades.length; i++) {
sum += grades[i];
}
return sum / grades.lenght;
}

function getGradeLetter(score) {
if (score >= 90)
return "A";
if (score >= 80)
return "B";
if (score >= 70)
return "C";
if (score >= 60)
return "D";
else
return "F";
}

let studentScores = [85, 92, 78, "95", 88];
let avg = calculateAverage(studentScores);
console.log("Average: " + avg);
console.log("Grade: " + getGradeLetter(avg));

let result = calculateAverage(10, 20, 30);
