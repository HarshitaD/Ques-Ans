#!/usr/bin/env bash
cd ~/Desktop/CMU_Ques/QuestionGeneration
cat '/home/harshita/Desktop/Question_Generation/Input_new.txt' |
java -Xmx1200m -cp question-generation.jar \
	edu/cmu/ark/QuestionAsker \
	--verbose --model models/linear-regression-ranker-reg500.ser.gz \
	--prefer-wh --max-length 30 --downweight-pro >  '/home/harshita/Desktop/Question_Generation/CMU.txt' -nopath
