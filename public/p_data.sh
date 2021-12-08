if [ -e "input_d_$1.txt" ];
then
	cat "input_d_$1.txt"
	exit
fi
#AOC_SESSION needs to be set from shell
python -c "from aocd.models import Puzzle;puzzle = Puzzle(year=2021, day=$1);print(puzzle.input_data);" > "input_d_$1.txt"
cat "input_d_$1.txt"
