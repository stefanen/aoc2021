./p_data.sh 13 | head -n -13  \
	| awk -F',' '$1<655 {print $1","$2} $1>655 {print (655*2-$1)","$2}' | sort | uniq \
	| awk -F',' '$2<447 {print $1","$2} $2>447 {print $1","(447*2-$2)}' | sort | uniq \
	| awk -F',' '$1<327 {print $1","$2} $1>327 {print (327*2-$1)","$2}' | sort | uniq \
	| awk -F',' '$2<223 {print $1","$2} $2>223 {print $1","(223*2-$2)}' | sort | uniq \
	| awk -F',' '$1<163 {print $1","$2} $1>163 {print (163*2-$1)","$2}' | sort | uniq \
	| awk -F',' '$2<111 {print $1","$2} $2>111 {print $1","(111*2-$2)}' | sort | uniq \
	| awk -F',' '$1<81 {print $1","$2} $1>81 {print (81*2-$1)","$2}' | sort | uniq \
	| awk -F',' '$2<55 {print $1","$2} $2>55 {print $1","(55*2-$2)}' | sort | uniq \
	| awk -F',' '$1<40 {print $1","$2} $1>40 {print (40*2-$1)","$2}' | sort | uniq \
	| awk -F',' '$2<27 {print $1","$2} $2>27 {print $1","(27*2-$2)}' | sort | uniq \
	| awk -F',' '$2<13 {print $1","$2} $2>13 {print $1","(13*2-$2)}' | sort | uniq \
	| awk -F',' '$2<6 {print $1","$2} $2>6 {print $1","(6*2-$2)}' | sort | uniq

