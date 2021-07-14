var link = document.createElement("link");
document.head.appendChild(link);
link.href = "/static/contextmenu.css";
link.rel = "stylesheet";
document.onclick = hideMenu; 
document.oncontextmenu = rightClick;
window.onblur = hideMenu;

function hideMenu() { 
    document.querySelector(".context-menu").style.display = "none";
} 

function rightClick(e) { 
    e.preventDefault(); 
    if(document.querySelector(".context-menu").style.display == "block"){
        hideMenu(); 
    }
    else { 
        var menu = document.querySelector(".context-menu");  
        menu.style.display = 'block';
        menu.style.left = e.pageX + "px"; 
    	menu.style.top = e.pageY + "px"; 
    }
}