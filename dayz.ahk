Toggle := 1
;
$Up::
	if Toggle
	{		
		Send {w}
		Send {w down}
		Toggle := 0
	}
	else
	{
		Send {w up}
		Toggle := 1
	}
	return
