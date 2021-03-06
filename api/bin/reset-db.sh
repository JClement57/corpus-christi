#!/usr/bin/env bash

source ./venv/bin/activate

rm dev-db.sqlite
rm migrations/versions/*.py

flask db migrate
flask db upgrade
flask course new --prereq=6 "Alone low investment" "This is a fake course."
flask data load-all
# Creating More readable courses and diplomas
flask course new --offering="This is the honors section!" "Bible Lit 1" "Survey of the Old Testament"
flask course new --prereq="Bible Lit 1" --offering="This section focuses on the teachings of Jesus!" "Bible Lit 2" "Survey of the New Testament"
flask course new --prereq="Bible Lit 2" --offering="This is the early offering!" "Introduction to Church History" "Walks through time looking at different doctorines created by the Church."
flask course new --prereq="Introduction to Church History" --offering="This section focuses on ways to apply the Bible teachings to life!" "Contemporary Christian Belief" "Challenges Christians to apply teachings to daily life."
flask course new --offering="This is the late offering!" "Family Life" "Helps leaders of the family realize their role and other family members' roles through Christ."
flask course new --prereq="Family Life" --offering="Lunch meeting time." "Family Life II" "For those that want to explore the relational nature of Christ in family."
flask course new --offering="Walk and Talk" "Child of God" "For people young in their faith that want to learn about the inheritence that is given to them in heaven."
flask account new --first="Fred" --last="Ziffle" username password
flask course new --prereq=6 --offering="Around happy fast" "Alone low investment" "blah blah blah"
flask diploma new "Above" "blah blah blah"
flask account new --first="Quality" --last="Assurance" Cytest password
