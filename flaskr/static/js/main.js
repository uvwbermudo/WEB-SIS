const csrf = $('#csrf_token').val();

$('document').ready(function(){

    $('#college_searchbar').on('input', search_college)
    $('#college_filter').on('change', search_college)
    $('#course_searchbar').on('input',course_search)
    $('#course_filter').on('change',course_search)
})




function course_search(){
    var search_query = $('#course_searchbar').val()
    var search_filter = $('#course_filter').val();
    const course_thead = $('#course_thead');
    const course_tbody = $('#course_tbody');  
    const course_tc = $('#course_tc');

    fetch('/course-search', {
        method: 'POST',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf,
        },
        body: JSON.stringify({ 
            search_query: search_query,
            search_filter: search_filter,
            }),
      }).then(response => (response.json()))
      .then(function(response) {
            console.log(response[0])
            course_tbody.html('')

      for(var i = 0; i<response[0].length; i++){
        course_tbody.append(
            '<tr>'+
            '<th scope="row" class="ps-5">'+response[0][i][0]+'</th>'+
            '<td>'+response[0][i][1]+'</td>'+
            '<td id="course_college'+response[0][i][0]+'"></td>'+
            
            '<td class="pe-0">'+
                '<a href="/course-edit/'+response[0][i][0]+'"class="btn btn-warning btn-sm my-1 me-1" role="button"'+ 'aria-pressed="true" data-bs-toggle="modal" data-bs-target="#editcourse'+response[0][i][0]+'" style="width:'+ '120px;">Edit</a>'+
  
                '<a href="/course-delete/'+response[0][i][0]+'" class="btn btn-danger btn-sm my-1" role="button"'+ 'aria-pressed="true" style="width: 120px;" data-bs-target="#confirmdelete'+response[0][i][0]+'"'+ 'data-bs-toggle="modal">Delete</a>'+
  
            '</td>'+
            '</tr>'
        )
        if (!response[0][i][2]){
            $('#course_college'+response[0][i][0]).html('<p class="fst-italic fw-light my-auto h-50">College Removed</p>')
        }
        else {
            $('#course_college'+response[0][i][0]).html(response[0][i][2])
        }
      }    
    })
    
}

function search_college(){
    var search_query = $('#college_searchbar').val();
    var search_filter = $('#college_filter').val();
    const college_thead = $('#college_thead');
    const college_tbody = $('#college_tbody');  
    const college_tc = $('#college_tc');
    fetch('/college-search', {
      method: 'POST',
      credentials: "include",
      headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf,
      },
      body: JSON.stringify({ 
          search_query: search_query,
          search_filter: search_filter,
          }),
    }).then(response => (response.json()))
    .then(function(response) {
        college_tbody.html('')

        for(var i = 0; i<response[0].length; i++){
          college_tbody.append(
          '<tr id="college_row">'+
              '<th scope="row" class="ps-5">'+response[0][i][0]+'</th>'+
              '<td>'+response[0][i][1]+'</td>'+
              '<td class="pe-0">'+
                  '<a href="/college-edit/'+response[0][i][0]+'"class="btn btn-warning btn-sm my-1 me-1" role="button"'+ 'aria-pressed="true" data-bs-toggle="modal" data-bs-target="#editcollege'+response[0][i][0]+'" style="width:'+ '120px;">Edit</a>'+
  
                  '<button class="btn btn-danger btn-sm my-1" type="button" aria-pressed="true" style="width: 120px;"'+ 'data-bs-target="#confirmdelete'+response[0][i][0]+'" data-bs-toggle="modal">Delete</button>'+
              '</td>'+
              '</tr>'
          )
      }      
  })
}

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
            if (response.status == 299){
                console.log('Successfully registered')
                window.location.replace(dest)    
            } else if( response.status == 497){
                console.log('Verified connection')
                return
            } 
            return response.json()
            

        })
        .then(function(responses) {
            responses[1].forEach(function(field){

                formfield = $('#'+field);
                formfieldnext = formfield.next();
                formfieldnext.html('');
                formfield.css({"border-color":""});
                if (field in responses[0]) {
                    formfield.css({"border-color":"red"});
                    formfieldnext.html(
                        "<span class=\"ms-auto float-end text-danger\">"+responses[0][field][0]+" <i class=\"bi-exclamation-circle-fill\"></i> </span>");
                } else{
                    if (responses[1].length < 5){
                        return
                    }
                    formfield.css({"border-color":"green"});
                    formfieldnext.html("<span class=\"ms-auto float-end text-success\">Looks Good! <i class=\"bi-check-circle-fill\"></i> </span>");
                    formfieldnext.css({"color":"green"});
                }
            })
            

        })
}


 
function verify_college(csrf, mode,hid=0) {
    item1 = $('#college_code')
    item2 = $('#college_name')
    if (mode == 1){
        item1 = $('div#editcollege'+hid+' #college_code')
        item2 = $('div#editcollege'+hid+' #college_name')
    } 

    fetch('/college-verify', {
        method: 'POST',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf
          },
        body: JSON.stringify({ 
            college_code: item1.val(),
            college_name: item2.val(), 
            hid: hid,
            mode: mode,
            }),
        })
        .then(response => {
            if (response.status == 299){
                console.log('Successfully Added College') 
                location.reload()
                return
            } else if( response.status == 497){
                console.log('Verified connection')
                return
            } 
            return response.json()
        })
        .then(function(responses) {
            responses[1].forEach(function(field){
                
                console.log(responses[0])
                if (field in responses[0]) {
                    
                    formfield = $('#'+field);
                    if (mode == 1){
                        $('div#confirm'+hid+' #back').click(); 
                        
                        formfield = $('div#editcollege'+hid+' #'+field)
                        console.log('div#editcollege'+hid+' #'+field)
                        console.log(formfield)
                    }
                    formfieldnext = formfield.next();
                    formfield.css({"border-color":"red"});
                    formfieldnext.html('');
                    formfieldnext.html(
                        "<span class=\"ms-auto float-end text-danger\">"+responses[0][field][0]+" <i class=\"bi-exclamation-circle-fill\"></i> </span>");
                } else{
                    formfield = $('.modal-body #'+field);
                    if (mode == 1){
                        formfield = $('div#editcollege'+hid+' #'+field)
                    }
                    formfieldnext = formfield.next();
                    formfield.css({"border-color":"green"});
                    formfieldnext.html("<span class=\"ms-auto float-end text-success\">Looks Good! <i class=\"bi-check-circle-fill\"></i> </span>");
                    formfieldnext.css({"color":"green"});
                }
            })
        })
}


function verify_course(mode,hid=0) {
    course_code = $('div#addcourse #course_code')
    course_name = $('div#addcourse #course_name')
    college_origin = $('div#addcourse #college')
    if (mode == 1){
        course_code = $('div#editcourse'+hid+' #course_code')
        course_name = $('div#editcourse'+hid+' #course_name')
        college_origin = $('div#editcourse'+hid+' #college')

    } 

    fetch('/course-verify', {
        method: 'POST',     
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf
          },
        body: JSON.stringify({ 
            course_code: course_code.val(),
            course_name: course_name.val(),
            college: college_origin.val(),
            hid: hid,
            mode: mode,
            }),
        })
        .then(response => {
            if (response.status == 299){
                console.log('Successfully Added Course') 
                location.reload()
                return
            } else if( response.status == 497){
                console.log('Verified connection')
                return
            } 
            return response.json()
        })
        .then(function(responses) {
            responses[1].forEach(function(field){
                console.log(responses)
                console.log(responses[0])
                console.log('HEERE')
                if (field == 'college'){
                    return;
                }
                if (field in responses[0]) {
                    
                    formfield = $('#'+field);
                    if (mode == 1){
                        $('div#confirm'+hid+' #back').click(); 
                        
                        formfield = $('div#editcourse'+hid+' #'+field)
                        console.log('div#editcourse'+hid+' #'+field)
                        console.log(formfield)
                    }
                    formfieldnext = formfield.next();
                    formfield.css({"border-color":"red"});
                    formfieldnext.html('');
                    formfieldnext.html(
                        "<span class=\"ms-auto float-end text-danger\">"+responses[0][field][0]+" <i class=\"bi-exclamation-circle-fill\"></i> </span>");
                } else {
                    formfield = $('.modal-body #'+field);
                    if (mode == 1){
                        formfield = $('div#editcourse'+hid+' #'+field)
                    }
                    formfieldnext = formfield.next();
                    formfield.css({"border-color":"green"});
                    formfieldnext.html("<span class=\"ms-auto float-end text-success\">Looks Good! <i class=\"bi-check-circle-fill\"></i> </span>");
                    formfieldnext.css({"color":"green"});
                }
            })
        })
}