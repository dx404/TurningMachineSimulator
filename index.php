<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8" >
	<title> Automata Web Simulator </title>
	<link rel="stylesheet" type="text/css" href="CSS/body.css" >
	<link rel="stylesheet" type="text/css" href="CSS/index.css" >
	<script src="../../frameworks/jquery.js"></script>
</head>

<body>
	<h1>Single-Tape Non-deterministic Turing Machine Simulator</h1>
<form id="inOut" name="inOut" action="." method="post">
	<table><tr>
	<td>
	<textarea id="formInput" name="formInput" rows="50" cols="50">
<?php 
	if(isset($_POST[formInput])){
		echo $_POST[formInput];
	}
	else { ?>
----Transition Table----
----(state, readSymbol, nextState, writeSymbol, move)----
q0 0 q1 0 R
q0 1 q1 0 R
q0 B q1 0 R
q1 0 q1 1 R
q1 0 q2 0 L
q1 1 q1 1 R
q1 1 q2 1 L
q1 B q1 1 R
q1 B q2 B L
q2 0 qf 0 R
q2 1 q2 1 L

----Initial Tape Data, State and Head Position----
1010 q0 0

----Final State---
qf

----Num of Steps---
10
<?php } ?>
	</textarea>
	</td>
	
	<td>
		<button type="submit">Run It</button>
	</td>
	
	<td>
		<textarea rows="50" cols="90">
<?php
	$formInput = $_POST["formInput"];
	echo shell_exec("echo '$formInput' | python TM.py"); 
?>
		</textarea>
	</td>
	</tr></table>
</form>
</body>