./p_data.sh 8 | 
	awk 'function convert(bd,cf,input) {if (length(input)==2) return 1; if (length(input)==3) return 7; if (length(input)==4) return 4; if (length(input)==7) return 8; type=contains(bd,cf,input); if (length(input)==6 && type=="both") return 9; if (length(input)==6 && type=="cf") return 0; if (length(input)==6) return 6; if (length(input)==5 && type=="cf") return 3; if (length(input)==5 && type=="bd") return 5; if (length(input)==5) return 2; return -1;} function contains(bd,cf,test) {bd_test=test; cf_test=test; gsub("["cf"]","",cf_test); gsub("["bd"]","",bd_test); if (length(bd_test)+1<length(test) && length(cf_test)+1<length(test) ) return "both"; if (length(bd_test)+1<length(test)) return "bd"; if (length(cf_test)+1<length(test)) return "cf"; return "none"} {for(i=1; i<=10; i++) {if(length($i)==2) cf=$i; if(length($i)==4) bd=$i;}} {gsub("["cf"]","",bd);} {print convert(bd,cf,$12)""convert(bd,cf,$13)""convert(bd,cf,$14)""convert(bd,cf,$15)} END {print SUM}' | awk '{SUM=SUM+$0} END {print SUM}'
