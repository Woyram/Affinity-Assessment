
// Login Function
$('#btnLoginUser').click(function(e) {
    show_loader();
    e.preventDefault();

    var username = $("#txtUsername").val();
    var password = $("#txtPassword").val();

    var data = new FormData();

    data.append("username", username);
    data.append("password", password);

    $.postJSON("/admins/login", data, function(data){

        if (data.code == "00") {
            displaySuccessMsg(data.msg);
            window.location = "/dashboard";
        }
        else{
            displayErrorMsg(data.msg);
            console.log("No");
        }
      });
});

function generateCoupons(){

    $("#uploadCustomers").modal("show");

    var data = new FormData();

    const id = "#kt_modal_upload_dropzone";
        const dropzone = document.querySelector(id);

        // set the preview element template
        var previewNode = dropzone.querySelector(".dropzone-item");
        previewNode.id = "";
        var previewTemplate = previewNode.parentNode.innerHTML;
        previewNode.parentNode.removeChild(previewNode);

        var myDropzone = new Dropzone(id, { // Make the whole body a dropzone
            url: "path/to/your/server", // Set the url for your upload script location
            parallelUploads: 10,
            previewTemplate: previewTemplate,
            maxFilesize: 1, // Max filesize in MB
            autoProcessQueue: false, // Stop auto upload
            autoQueue: false, // Make sure the files aren't queued until manually added
            previewsContainer: id + " .dropzone-items", // Define the container to display the previews
            clickable: id + " .dropzone-select" // Define the element that should be used as click trigger to select files.
        });

        myDropzone.on("addedfile", function (file) {
            // Hook each start button
            file.previewElement.querySelector(id + " .dropzone-start").onclick = function () {
                // myDropzone.enqueueFile(file); -- default dropzone function

                // Process simulation for demo only
                const progressBar = file.previewElement.querySelector('.progress-bar');
                progressBar.style.opacity = "1";
                var width = 1;
                var timer = setInterval(function () {
                    if (width >= 100) {
                        myDropzone.emit("success", file);
                        myDropzone.emit("complete", file);
                        clearInterval(timer);
                    } else {
                        width++;
                        progressBar.style.width = width + '%';
                    }
                }, 20);
            };

            const dropzoneItems = dropzone.querySelectorAll('.dropzone-item');
            dropzoneItems.forEach(dropzoneItem => {
                dropzoneItem.style.display = '';
            });
            dropzone.querySelector('.dropzone-upload').style.display = "inline-block";
            dropzone.querySelector('.dropzone-remove-all').style.display = "inline-block";
        });

        // Hide the total progress bar when nothing's uploading anymore
        myDropzone.on("complete", function (file) {
            const progressBars = dropzone.querySelectorAll('.dz-complete');
            setTimeout(function () {
                progressBars.forEach(progressBar => {
                    progressBar.querySelector('.progress-bar').style.opacity = "0";
                    progressBar.querySelector('.progress').style.opacity = "0";
                    progressBar.querySelector('.dropzone-start').style.opacity = "0";
                });
            }, 300);
        });

        // Setup the buttons for all transfers
        dropzone.querySelector(".dropzone-upload").addEventListener('click', function () {
            // myDropzone.processQueue(); --- default dropzone process

            // Process simulation for demo only
            myDropzone.files.forEach(file => {
                const progressBar = file.previewElement.querySelector('.progress-bar');
                progressBar.style.opacity = "1";
                var width = 1;
                var timer = setInterval(function () {
                    if (width >= 100) {
                        myDropzone.emit("success", file);
                        myDropzone.emit("complete", file);
                        clearInterval(timer);
                    } else {
                        width++;
                        progressBar.style.width = width + '%';
                    }
                }, 20);

                var data = new FormData();
                data.append("csv_file", file);

                $.ajax({
                    url: "/coupons/generate-coupons",
                    data: data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    method: "POST",
                    type: "POST",
                    success: function(response) {

                        if (response.code == "00") {
                            console.log("YES");
                            $("#uploadCustomers").modal("hide");
                            fireAlert(response.msg, "success");
                            setTimeout(function(){
                                location.reload();
                            }, 2000);
                        } else {
                            console.log("NO");
                            fireAlert(response.msg, "error");
                            setTimeout(function(){
                                location.reload();
                            }, 2000);
                        }
                    },
                });
            });
        });

        // Setup the button for remove all files
        dropzone.querySelector(".dropzone-remove-all").addEventListener('click', function () {
            Swal.fire({
                text: "Are you sure you would like to remove all files?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: "Yes, remove it!",
                cancelButtonText: "No, return",
                customClass: {
                    confirmButton: "btn btn-primary",
                    cancelButton: "btn btn-active-light"
                }
            }).then(function (result) {
                if (result.value) {
                    dropzone.querySelector('.dropzone-upload').style.display = "none";
                    dropzone.querySelector('.dropzone-remove-all').style.display = "none";
                    myDropzone.removeAllFiles(true);
                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Your files was not removed!.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary",
                        }
                    });
                }
            });
        });

        // On all files completed upload
        myDropzone.on("queuecomplete", function (progress) {
            const uploadIcons = dropzone.querySelectorAll('.dropzone-upload');
            uploadIcons.forEach(uploadIcon => {
                uploadIcon.style.display = "none";
            });
        });

        // On all files removed
        myDropzone.on("removedfile", function (file) {
            if (myDropzone.files.length < 1) {
                dropzone.querySelector('.dropzone-upload').style.display = "none";
                dropzone.querySelector('.dropzone-remove-all').style.display = "none";
            }
        });
}



// Get Coupons
function get_coupons(upload_id){
    console.log(upload_id);
    window.location = "/coupons/details/"+upload_id;
}

function showLoader(msg){

    console.log("Loader");

    if (msg == '' || msg == undefined){
          msg="Loading...";
        }
        $(".button").html('<div class="spinner-grow text-primary" role="status">'+
                        '<span class="visually-hidden">Loading...</span>'+
                        '</div>')
        $(".button").show("fast");

}

function showMessage(){
    var e = $(".responses");
    e.length && e.on("click", function(e) {
        e.preventDefault();
        var l = $(this);
        l.closest(".card").block({
            message: '<div class="sk-fold sk-primary"><div class="sk-fold-cube"></div><div class="sk-fold-cube"></div><div class="sk-fold-cube"></div><div class="sk-fold-cube"></div></div><h5>LOADING...</h5>',
            css: {
                backgroundColor: "transparent",
                border: "0"
            },
            overlayCSS: {
                backgroundColor: $("html").hasClass("dark-style") ? "#000" : "#fff",
                opacity: .55
            }
        }), setTimeout(function() {
            l.closest(".card").unblock(), l.closest(".card").find(".card-alert").length && l.closest(".card").find(".card-alert").html('<div class="alert alert-danger alert-dismissible fade show" role="alert"><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button><strong>Holy grail!</strong> Your success/error message here.</div>')
        }, 2500)
    })
}


$.postJSON = function(url, data, callback) {
  return jQuery.ajax({
      type: "POST",
      url: url,
      data: data,
      dataType: 'json',
      processData: false,
      contentType: false,
      success: callback,
      error: onAjaxError,
      timeout: 50000,
      cache: false
  });
};

$.putJSON = function(url, data, callback) {
    return jQuery.ajax({
        type: "PUT",
        url: url,
        contentType: "application/json",
        data: data,
        dataType: "json",
        success: callback,
        error: onAjaxError,
        timeout: 50000,
        cache: false,
    });
};

$.getJSON = function(url, data, callback) {
    return jQuery.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        data: data,
        dataType: "json",
        success: callback,
        error: onAjaxError,
        timeout: 50000,
        cache: false,
    });
};

$.deleteJSON = function(url, data, callback) {
    return jQuery.ajax({
        type: "DELETE",
        url: url,
        contentType: "application/json",
        data: data,
        dataType: "json",
        success: callback,
        error: onAjaxError,
        timeout: 50000,
        cache: false,
    });
};

function onAjaxError(xhr, status, error){
//    hide_loader();
    displayErrorMsg(error);
}

function displayErrorMsg(msg){
  //hide loader
  //hide_loader();

    $(".response").html("<div align='center' class='alert alert-danger' role='alert'><p class='text-left'>"+
        msg+"</p></div>");
    setTimeout(function() {
        $(".response").html('');
    }, 30000);
}

function displaySuccessMsgModal(msg){
    //hide loader
    //hide_loader();
    $(".selectPlacement").html("<div class='bs-toast toast toast-placement-ex m-2' role='alert' aria-live='assertive' aria-atomic='true' data-delay='2000'><div class='toast-header'></div><i class='bx bx-bell me-2'></i><div class='me-auto fw-semibold'>Bootstrap</div><small>11 mins ago</small><button type='button' class='btn-close' data-bs-dismiss='toast' aria-label='Close'></button></div><div class='toast-body'>"+msg+".</div></div>");
    setTimeout(function() {
        $(".selectPlacement").html('');
    }, 30000);
}

function displaySuccessMsg(msg){
  //hide loader
  //hide_loader();

  $(".response").html("<div align='center' class='alert alert-success' role='alert'><p class='text-left'>"+
        msg+"</p></div>");
    setTimeout(function() {
        $(".response").html('');
    }, 30000);
}

function fireAlert(msg, type){
    Swal.fire({
        title: msg,
        icon: type,
        customClass: {
            confirmButton: "btn btn-primary"
        },
        buttonsStyling: !1
    });
}

function show_loader(msg){
    if (msg == '' || msg == undefined){
      msg="Loading...";
    }
    $(".loader").html('<div align="center" style="margin:0 auto; margin-top:30px;" class="text-center">'+
                    '<div class="-spinner-ring -error-"></div>'+
                    '<h5>'+msg+'</h5>'+
                    '</div>')
    $(".loader").show("fast");
}
