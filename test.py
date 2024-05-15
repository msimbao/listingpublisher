sections_dictionary = {
    42378910 : "Book Lover",
    42393967 : "Food",
    42395337 : "Funny Other",
    42395341 : "Hobby / Passion / Other",
    42395343 : "Sport",
    42395347 : "Farm Life / Country",
    42395351 : "Introvert",
    42381728 : "Conditions",
    42395359 : "Camping / Lake / Travel",
    42381732 : "Nurse / Dentist / Doctor",
    42381736 : "Real Estate",
    42381740 : "Flower / Plant Lover",
    42381742 : "Dog / Cat / Animal",
    42381746 : "Baking / Cookie Lover",
    42381752 : "Teacher / Therapist",
    42381754 : "Inspirational",
    42381756 : "Pregnancy Announcement",
    42381760 : "Wedding Bridal Party",
    42395385 : "Mom, Dad, Family"
}

test = '42393967'
print(test)
print(type(test))
section = test.replace("'","")
print(section)
print(type(section))
print(sections_dictionary[int('42393967')])