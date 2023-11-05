/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // upload form
    document.querySelector('#upload-form').onsubmit = function() {

        const files = document.querySelector('#image-file');
        // const imageFile = image.files[0];
        console.log(files)
      
        fetch('/upload', {
          method: 'POST',
          body: JSON.stringify({
              files: files
          })
        })
        // .then(res => { console.log(res); return res.text(); })
        // .then(txt => console.log(txt))
        .then(response => response.json())
        .then(path => {
            // Print result
            console.log(path);
            // const iframe = document.querySelector("#text-output")
            // console.log(iframe)
            // iframe.src = path

            // PDFObject.embed(path, "#text-output");

            // paragraph.forEach(paragraphs => {

            //     // article
            //     const article = document.createElement('article');
            //     article.className = "list-group-item";
            //     article.id = `p${post.id}`;
        
            //     // content
            //     const content = document.createElement('p');
            //     content.innerHTML = post.text;
        
            //     article.append(content);
        
            //     section.append(article)
        
            //     // console.log(post)
            // })
        }).catch(err => console.error(err));

        const embed = document.querySelector("#text-output")
        console.log(embed)
    }
});

/*
function load_text(file) {
    fetch(path)
    .then(response => response.json())
    .then(paragraphs => {
        console.log(paragraphs)
        const section = document.querySelector("#section")

        // clear section first
        section.innerHTML = ""

        paragraph.forEach(paragraphs => {

        // article
        const article = document.createElement('article');
        article.className = "list-group-item";
        article.id = `p${post.id}`;

        // content
        const content = document.createElement('p');
        content.innerHTML = post.text;

        article.append(content);

        section.append(article)

        // console.log(post)
        })
    })
    .catch(err => console.error(err));
    };
}

*/