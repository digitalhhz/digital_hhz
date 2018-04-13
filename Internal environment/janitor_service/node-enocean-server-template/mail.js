var nodemailer = require('nodemailer');

//var subject="Raum125 Info";
//var message;

// create reusable transporter object using the default SMTP transport
var transporter = nodemailer.createTransport({
 host: 'mail.gmx.com',
 port: 587,
 tls: {
     ciphers:'SSLv3',
     rejectUnauthorized: false
 },
 debug:true,
     auth: {
     user: 'hhz.raum125@gmx.de',
     pass: 'Password42'
 }
});

var sendMail = (subject, message) => {
  // setup e-mail data with unicode symbols
  var mailOptions = {
      from: '"Herman Hollerith" <hhz.raum125@gmx.de>', // sender address
      to: 'hhz.raum125@gmx.de', // list of receivers
      subject: subject, // Subject line
      text: message, // plaintext body
      html: '<p>'+message+'</p>' // html body
  };

  // send mail with defined transport object
  transporter.sendMail(mailOptions, function(error, info){
      if(error){
          return console.log(error);
      }
      console.log('Message sent: ' + info.response);
  });
}
