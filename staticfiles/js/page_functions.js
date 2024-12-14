function check_date(date){
const d = new Date();
let text = d.toISOString().slice(0,10);
if (date == d){ return true}else{ return false}
}
