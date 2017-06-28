
#!/usr/bin/env bash
cd ~/Desktop/CMU_Ques/QuestionGeneration
cat $1 |
java -Xmx1200m -cp question-generation.jar \
	edu/cmu/ark/QuestionAsker \
	--verbose --model models/linear-regression-ranker-reg500.ser.gz \
	--prefer-wh --max-length 30 --downweight-pro >  $2 -nopath
