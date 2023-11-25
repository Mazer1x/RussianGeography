
var backend = null;
new QWebChannel(qt.webChannelTransport, function (channel) {
    backend = channel.objects.backend;
});
del = ()=>{
    let el1 = document.querySelector('.leaflet-control-attribution');
    let el2 = document.querySelector('#legend');
    
    
    el1.remove();
    el2.remove();
    number = 1
    target = 10
    let interval = setInterval(function() {
        document.querySelector('body').style.opacity = number/10;
        if (number >= target) clearInterval(interval);
        number+=1;
    }, 70);
    
    a = document.querySelectorAll('.leaflet-marker-pane img');
    for(let i =0; i < a.length;i++){
        a[i].addEventListener("click", function(){
            try{
                backend.value = i;
            }catch{
                console.log(i);
            }
        });
    }
    obl = document.querySelectorAll('.leaflet-overlay-pane svg g path')
    for(let i =0; i < obl.length;i++){
        obl[i].addEventListener("dblclick", function(){
            try{
                backend.value = 'A'+i;
            }catch{
                console.log('A'+i);
            }
        });
    }
    
}