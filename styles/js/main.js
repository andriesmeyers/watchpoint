(function(){ 
    var reqCategory = getParameterByName('category');
    setView(reqCategory);
    var currentCategory;
    var categories = document.querySelectorAll('.category-list .list-group-item');
    for(var i=0; i<categories.length; i++){
        categories[i].addEventListener('click', switchView);
    }
    
    function getParameterByName(name, url) {
        if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }

    function switchView(e){
        category = this.textContent.toLowerCase().replace(/\s/g, "").replace('&', 'en').replace(',', '').replace('\'', '');
        
        if (currentCategory != category){
            var activeItem = e.currentTarget.parentNode.getElementsByClassName('active');
            if(activeItem.length > 0)
                activeItem[0].classList.remove('active');
            e.currentTarget.classList.add('active');
            document.querySelectorAll('.sub-list').forEach(elem => {
                elem.style.display = "none";
            });
            document.querySelector('.sub-list-'+ category).setAttribute('style', 'display:block !important');
        }
        currentCategory = category;
    }
    function setView(category){
        category = decodeString(category);
        if (currentCategory != category){
            var activeItem = document.getElementsByClassName('category-' + category);
            if(activeItem.length > 0)
                activeItem[0].classList.add('active');
            document.querySelector('.sub-list-'+ category).setAttribute('style', 'display:block !important');
        }
        currentCategory = category;
    }
    function decodeString(string){
        string = string.toLowerCase();
        string = string.replace('&', 'en');
        string = string.replace(',', '');
        string = string.replace('\'', '');
        string = string.replace(/\s/g, "");
        return string;
    }
})();