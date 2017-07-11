$(function() {
  
 $("#register-form").validate({
    
        // Specify the validation rules
        rules: {
            firstname: "required",
            mobile: "required",
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6
            },
            agree: "required"
        },
        
        // Specify the validation error messages
        messages: {
            firstname: "Please enter your first name",
            mobile: "Please enter your mobile number",
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long"
            },
            email: "Please enter a valid email address",
            
        },
         submitHandler: function(form) {
            form.submit();
        }
    });

  });
  