
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


// Send Reset Code.
$('#btnSendPasswordCode').click(function(e) {
    show_loader();
    e.preventDefault();

    var userMobile = $("#txtUserphone").val();

    var data = new FormData();

    data.append("userMobile", userMobile);

    $.postJSON("/admins/reset-password", data, function(data){

        if (data.code == "00") {
            displaySuccessMsg(data.msg);
            window.location = "/auth/set-password";
        }
        else{
            displayErrorMsg(data.msg);
            console.log("No");
        }
      });
});


// Reset Code.
$('#btnSetUserPassword').click(function(e) {
    show_loader();
    e.preventDefault();

    var password = $("#txtUserPassword").val();
    var userPassword = $("#txtUserConfPassword").val();
    var code = $("#txtOTPCode").val();

    var data = new FormData();

    data.append("password", password);
    data.append("userPassword", userPassword);
    data.append("code", code);

    $.postJSON("/admins/set-password", data, function(data){

        if (data.code == "00") {
            displaySuccessMsg(data.msg);
            window.location = "/";
        }
        else{
            displayErrorMsg(data.msg);
            console.log("No");
        }
      });
});

// Reset Password
$('#resetPassword').click(function(e) {
    e.preventDefault();

    var oldPassword = $("#txtOldPassword").val();
    var authCurrentPassword = $("#txtAuthCurrentPassword").val();
    var authConfirmPassword = $("#txtAuthConfirmPassword").val();

    var data = new FormData();

    data.append("old_password", oldPassword);
    data.append("current_password", authCurrentPassword);
    data.append("confirm_password", authConfirmPassword);

    $.ajax({
        url: "/auth/changePassword",
        data: data,
        beforeSend: function(){
            $("#loader").show();
            $("#btnAddUser").hide();
        },
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
});


// Add User
$('#addDevotion').click(function(e) {
    e.preventDefault();

    var devotionDescription = $(".ql-editor").html();

    var devotionTitle = $("#txtDevotionTitle").val();
    var devotionDate = $("#txtDevotionDate").val();
    var devotionScripture = $("#txtDevotionScripture").val();
    var devotionScriptureText = $("#txtDevotionScriptureText").val();
    var devotionStatus = $("#txtDevotionStatus").val();
    var devotionPrayer = $("#txtDevotionPrayer").val();
    var furtherReading = $("#txtDevotionFurtherReading").val();
    var bibleInOneYear = $("#txtDevotionBibleInOneYear").val();

    var data = new FormData();

    $.each(jQuery("#selected_image")[0].files, function(i, file) {
        data.append("file", file);
    });

    data.append("devotion_title", devotionTitle);
    data.append("devotion_date", devotionDate);
    data.append("devotion_scripture", devotionScripture);
    data.append("devotion_scripture_text", devotionScriptureText);
    data.append("devotion_description", devotionDescription);
    data.append("devotion_status", devotionStatus);
    data.append("devotion_prayer", devotionPrayer);
    data.append("further_reading", furtherReading);
    data.append("bible_in_one_year", bibleInOneYear);

    $.ajax({
        url: "/devotions/add-devotion",
        data: data,
        beforeSend: function(){
            $("#loader").show();
            $("#btnAddUser").hide();
        },
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
});

$('#btnAddSystemUser').click(function(e) {
    e.preventDefault();

    var firstname = $("#txtUserSysFirstName").val();
    var othername = $("#txtUserSysOtherName").val();
    var lastname = $("#txtUserSysLastName").val();
    var username = $("#txtUserSysUsername").val();
    var dob = $("#txtUserSysDoB").val();
    var role = $("#txtUserSysRole").val();
    var email = $("#txtUserSysEmail").val();
    var mobileNumber = $("#txtUserSysMobile").val();

    var data = new FormData();

    data.append("firstname", firstname);
    data.append("othername", othername);
    data.append("lastname", lastname);
    data.append("username", username);
    data.append("dob", dob);
    data.append("role", role);
    data.append("email", email);
    data.append("mobileNumber", mobileNumber);

    $.ajax({
        url: "/system/add-system-users",
        data: data,
        beforeSend: function(){
            $("#loader").show();
            $("#btnAddSystemUser").hide();
        },
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
});


// Get Consignment Details
function get_devotion_details(devotion_id){
    window.location = "/devotions/details/"+devotion_id;
}

// Add Transaction
$('#btnAddTransaction').click(function(e) {
    e.preventDefault();

    var user = $("#txtAddTransactionUser").val();
    var payment = $("#txtAddTransactionPayment").val();
    var paymentType = $("#txtAddTransactionPaymentType").val();
    var momoRef = $("#txtAddTransactionMomoRef").val();
    var transType = $("#txtAddTransactionTransactionType").val();
    var amount = $("#txtAddTransactionAmount").val();

    var data = new FormData();

    data.append("user", user);
    data.append("payment", payment);
    data.append("paymentType", paymentType);
    data.append("momoRef", momoRef);
    data.append("transType", transType);
    data.append("amount", amount);

    $.ajax({
        url: "/transactions/add-transaction",
        data: data,
        beforeSend: function(){
            $("#exloader").show();
            $("#loader").show();
            $("#btnAddTransaction").hide();
        },
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
});

// Deactivate User
$('#btnDeActivateUser').click(function(e) {

    var user_id = $("#txtUpUserID").val();

    $.ajax({
        url: "/users/deactivate/"+user_id,
        cache: false,
        beforeSend: function(){
            $("#exxloader").show();
            $("#btnDeActivateUser").hide();
        },
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });

});

// Approve Loan
$('#btnApproveLoan').click(function(e) {

    var loanId = $("#txtLoanID").val();

    var data = new FormData();
    data.append("status", "Approved");

    $.ajax({
        url: "/loans/approve/"+loanId,
        data: data,
        beforeSend: function(){
            $("#loader").show();
            $("#exloader").show();
            $("#btnApproveLoan").hide();
        },
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });

});

// Deny Loan
$('#btnDenyLoan').click(function(e) {

    var loanId = $("#txtLoanID").val();

    var data = new FormData();
    data.append("status", "Denied");

    $.ajax({
        url: "/loans/approve/"+loanId,
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });

});

// Upload Signed Documents
$('#btnAddLoanSignedDocs').click(function(e) {

    var loan_id = $("#txtLoanID").val();
    console.log(loan_id);
    var data = new FormData();

    $.each(jQuery("#loanDocuments")[0].files, function(i, file) {
        data.append("signed_loan_documents", file);
    });

    $.ajax({
        url: "/loans/uploadSignedDocs/"+loan_id,
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });

});

// Delete System User.
function deleteSystemUser(user_id){

    $.ajax({
        url: "/system/delete-system-users/"+user_id,
        data: user_id,
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
}

// Send SMS
$('#btnSendSMS').click(function(e) {
    e.preventDefault();

    var user = $("#txtSMSUser").val();
    var message = $("#txtSMSMessage").val();

    var data = new FormData();

    data.append("user", user);
    data.append("message", message);

    $.ajax({
        url: "/system/send-sms",
        data: data,
        beforeSend: function(){
            $("#loader").show();
            $("#btnSendSMS").hide();
        },
        cache: false,
        contentType: false,
        processData: false,
        method: "POST",
        type: "POST",
        success: function(response) {
            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
});


// Get Consignment Details
function get_loan_details(loan_id){

    window.location = "/loans/details/"+loan_id;
}


// Get Consignment Details
function get_user_details(user_id){

    window.location = "/users/details/"+user_id;

}

function deleteDevotion(devotion_id){
    $.ajax({
        url: "/devotions/delete-devotion/"+devotion_id,
        cache: false,
        contentType: false,
        processData: false,
        method: "GET",
        type: "GET",
        success: function(response) {

            if (response.code == "00") {
                console.log("YES");
                fireAlert(response.msg, "success");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            } else {
                console.log("NO");
                fireAlert(response.msg, "error");
                setTimeout(function(){
                    location.reload();
                }, 3000);
            }
        },
    });
}

function getTransaction(trans_id){

    $.ajax({
        url: "/transactions/getTransaction/"+trans_id,
        cache: false,
        contentType: false,
        processData: false,
        method: "GET",
        type: "GET",
        success: function(response) {

            if (response.code == "00") {
                console.log("YES");

                document.getElementById('transUserName').innerHTML = response.data.lastname+" "+response.data.firstname;
                document.getElementById('accountNumberText').innerHTML = response.data.account_id;
                document.getElementById('savingsText').innerHTML = response.data.account_type;
                document.getElementById('transactionTypeText').innerHTML = response.data.trans_type;
                document.getElementById('paymentTypeText').innerHTML = response.data.payment_type;
                document.getElementById('referenceID').innerHTML = response.data.reference_id;
                document.getElementById('amount').innerHTML = "<b>GHC "+response.data.amount+"</b>";

                $("#modalToggle").modal("show");
            } else {
                console.log("NO");
            }
        },
    });
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

// Profile Image Upload
function displayImage(input){
    if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#imagePreview').attr('src', e.target.result).width("100%").height("100%");
    };

    reader.readAsDataURL(input.files[0]);
  }
}

// Profile Image Upload
function displayEditedImage(input){
    if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#uploadedAvatar').attr('src', e.target.result);
      $('#defaultAvatar').attr('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}

function renderTransactionGraph(transData){

  let cardColor, headingColor, axisColor, shadeColor, borderColor;

  cardColor = "#fff";
  headingColor = "#566a7f";
  axisColor = "#a1acb8";
  borderColor = "#eceef1";

  // Total Revenue Report Chart - Bar Chart
  // --------------------------------------------------------------------
  const totalRevenueChartEl = document.querySelector('#transactionGraph'),
    totalRevenueChartOptions = {
      series: [
        {
          name: '2024',
          data: transData
        }
      ],
      chart: {
        height: 300,
        stacked: true,
        type: 'bar',
        toolbar: { show: false }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '50%',
          borderRadius: 12,
          startingShape: 'rounded',
          endingShape: 'rounded'
        }
      },
      colors: ["#1c439a", "#03c3ec"],
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth',
        width: 6,
        lineCap: 'round',
        colors: [cardColor]
      },
      legend: {
        show: true,
        horizontalAlign: 'left',
        position: 'top',
        markers: {
          height: 8,
          width: 8,
          radius: 12,
          offsetX: -3
        },
        labels: {
          colors: axisColor
        },
        itemMargin: {
          horizontal: 10
        }
      },
      grid: {
        borderColor: borderColor,
        padding: {
          top: 0,
          bottom: -8,
          left: 20,
          right: 20
        }
      },
      xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
        labels: {
          style: {
            fontSize: '13px',
            colors: axisColor
          }
        },
        axisTicks: {
          show: false
        },
        axisBorder: {
          show: false
        }
      },
      yaxis: {
        labels: {
          style: {
            fontSize: '13px',
            colors: axisColor
          }
        }
      },
      responsive: [
        {
          breakpoint: 1700,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '32%'
              }
            }
          }
        },
        {
          breakpoint: 1580,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '35%'
              }
            }
          }
        },
        {
          breakpoint: 1440,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '42%'
              }
            }
          }
        },
        {
          breakpoint: 1300,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '48%'
              }
            }
          }
        },
        {
          breakpoint: 1200,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '40%'
              }
            }
          }
        },
        {
          breakpoint: 1040,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 11,
                columnWidth: '48%'
              }
            }
          }
        },
        {
          breakpoint: 991,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '30%'
              }
            }
          }
        },
        {
          breakpoint: 840,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '35%'
              }
            }
          }
        },
        {
          breakpoint: 768,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '28%'
              }
            }
          }
        },
        {
          breakpoint: 640,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '32%'
              }
            }
          }
        },
        {
          breakpoint: 576,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '37%'
              }
            }
          }
        },
        {
          breakpoint: 480,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '45%'
              }
            }
          }
        },
        {
          breakpoint: 420,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '52%'
              }
            }
          }
        },
        {
          breakpoint: 380,
          options: {
            plotOptions: {
              bar: {
                borderRadius: 10,
                columnWidth: '60%'
              }
            }
          }
        }
      ],
      states: {
        hover: {
          filter: {
            type: 'none'
          }
        },
        active: {
          filter: {
            type: 'none'
          }
        }
      }
    };

    if (typeof totalRevenueChartEl !== undefined && totalRevenueChartEl !== null) {
    const totalRevenueChart = new ApexCharts(totalRevenueChartEl, totalRevenueChartOptions);
    totalRevenueChart.render();
  }


}

function displayImagez(input){
    if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#imagePreviewz').attr('src', e.target.result).width("100%").height("100%");
    };

    reader.readAsDataURL(input.files[0]);
  }
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
