var casper = require('casper').create();
 
casper.start(casper.cli.get(0), function() {    
    //this.wait(2000);
    this.echo(this.getHTML());
});
casper.run();
