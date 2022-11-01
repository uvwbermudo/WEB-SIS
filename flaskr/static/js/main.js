function verify_info(csrf, url, dest) {

    fetch(url, {
        method: 'POST',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf
          },
        body: JSON.stringify({ 
            email: $('#email').val(),
            password: $('#password').val(), 
            password2: $('#password2').val(),
            }),
        })
        .then(response => {
            if (response.status == 200){
                console.log('Successfully registered')
                window.location.replace(dest)    
            } else if( response.status == 497){
                console.log('Verified connection')
                return
            } else {
                return response.json()
            }

        })
        .then(function(responses) {
            responses[1].forEach(function(field){

                if (field in responses[0]) {
                    
                    formfield = $('#'+field);
                    formfieldnext = formfield.next();
                    formfield.css({"border-color":"red"});
                    formfieldnext.html('');
                    formfieldnext.html(
                        "<span class=\"ms-auto float-end text-danger\">"+responses[0][field][0]+" <i class=\"bi-exclamation-circle-fill\"></i> </span>");
                } else{
                    if (responses[1].length < 5){
                        return
                    }
                    formfield = $('#'+field);
                    formfieldnext = formfield.next();
                    formfield.css({"border-color":"green"});
                    formfieldnext.html("<span class=\"ms-auto float-end text-success\">Looks Good! <i class=\"bi-check-circle-fill\"></i> </span>");
                    formfieldnext.css({"color":"green"});
                }
            })
            

        })
}

function verify_college(csrf,url, dest) {
    fetch(url, {
        method: 'POST',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf
          },
        body: JSON.stringify({ 
            email: $('#email').val(),
            password: $('#password').val(), 
            password2: $('#password2').val(),
            }),
        })
}