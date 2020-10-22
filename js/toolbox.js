function toolbox(){
  var K_rack=document.getElementById("K_rack").value;
  var Q_rack=document.getElementById('Q_rack').value;
  var S_rack=document.getElementById('S_rack').value;

if((document.getElementById('RLlast').value)=="OPEN")
{
  document.getElementById('K_last').innerHTML= K_rack-(K_rack*0.1);
  document.getElementById('Q_last').innerHTML= Q_rack-(Q_rack*0.1);
  document.getElementById('S_last').innerHTML= S_rack-(S_rack*0.1);
}
else
{
  document.getElementById('K_last').innerHTML="NA";
  document.getElementById('Q_last').innerHTML="NA";
  document.getElementById('S_last').innerHTML="NA";
}

if((document.getElementById('RLopaque').value)=="OPEN")
{
  document.getElementById('K_opaque').innerHTML= K_rack-(K_rack*0.35);
  document.getElementById('Q_opaque').innerHTML= Q_rack-(Q_rack*0.35);
  document.getElementById('S_opaque').innerHTML= S_rack-(S_rack*0.35);
}
else
{
  document.getElementById('K_opaque').innerHTML= "NA";
  document.getElementById('Q_opaque').innerHTML= "NA";
  document.getElementById('S_opaque').innerHTML= "NA";
}

if((document.getElementById('RLgov').value)=="OPEN")
{
  document.getElementById('K_gov').innerHTML= 96;
  document.getElementById('Q_gov').innerHTML= 96;
  document.getElementById('S_gov').innerHTML= 96;
}
else
{
  document.getElementById('K_gov').innerHTML= "NA";
  document.getElementById('Q_gov').innerHTML= "NA";
  document.getElementById('S_gov').innerHTML= "NA";
}
}
