var populations = [];

this.patcher.newobject("router");

function createBpatcher(file,varname,args)
{
object = this.patcher.newdefault(
"bpatcher",
"@name", file,
"@border", 0,
"@varname", varname,
"@args", args,
"@orderfront", "1",
"@hint", varname,
"@embed", "0",
"@presentation", "0");
populations.push(object);
}

function deletePop(){
	post("deleteing");
	this.patcher.remove(populations[0]);
	populations.pop();
}