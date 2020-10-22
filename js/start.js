<script src="https://sdk.amazonaws.com/js/aws-sdk-2.7.16.min.js"></script>
AWS.config.update({
region: "us-east-1",
endpoint: "https://dynamodb.us-east-1.amazonaws.com",
accessKeyId: "AKIA6QNNY4GIGG72I7OQ",
secretAccessKey: "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"
});

var docClient = new AWS.DynamoDB.DocumentClient();

function start(){
 var K_rack=document.getElementById("K_rack").value;
 var Q_rack=document.getElementById('Q_rack').value;
 var S_rack=document.getElementById('S_rack').value;

 var K_last=document.getElementById("K_last").value;
 var Q_last=document.getElementById('Q_last').value;
 var S_last=document.getElementById('S_last').value;

 var K_opaque=document.getElementById("K_opaque").value;
 var Q_opaque=document.getElementById('Q_opaque').value;
 var S_opaque=document.getElementById('S_opaque').value;

 var K_gov=document.getElementById("K_gov").value;
 var Q_gov=document.getElementById('Q_gov').value;
 var S_gov=document.getElementById('S_gov').value;

var email= document.getElementById('email').value;
  var params = {
      TableName :"Game_data",
      Key:{
          "email" : email,
          "gametime" : 6
      },
      UpdateExpression: "set K_rack = :kr, Q_rack=:qr,S_rack=:sr",
      ExpressionAttributeValues:{
          ":kr":K_rack,
          ":qr":Q_rack,
          ":sr":S_rack
      },
      ReturnValues:"UPDATED_NEW"
  };

  console.log("Updating the item...");
  docClient.update(params, function(err, data) {
      if (err) {
          console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
      } else {
          console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
      }
  });
}
