<<<<<<< HEAD
document.getElementById('faq-dropdown').addEventListener('change', function() {
    var response;
    switch (this.value) {
        case 'Change my password':
            response = "To change your password, go to 'Manage Account' seen in the navigation bar at the top.";
            break;
        case 'View my activity history':
            response = "You can view your activity history in your 'My Logs' page.";
            break;
        case 'What kind of activities can I log in Renova?':
            response = 'In Renova, you can log any activity imaginable. These are user defined; go wild :)';
            break;
        case 'Delete my account':
            response = "To delete your account, please go to 'Manage Account' seen in the navigation bar at the top. there will be an option on the right to delete your account";
            break;
        default:
            response = '';
    }
    document.getElementById('faq-response').textContent = response;
=======
$(document).ready(function() {
    $('#faq-dropdown').change(function() {
        var response;

        switch (this.value) {
            case 'Change my password':
                response = "To change your password, go to 'Manage Account' seen in the navigation bar at the top.";
                break;
            case 'View my activity history':
                response = "You can view your activity history in your 'My Logs' page.";
                break;
            case 'What kind of activities can I log in Renova?':
                response = 'In Renova, you can log any activity imaginable. These are user defined; go wild :)';
                break;
            case 'Delete my account':
                response = "To delete your account, please go to 'Manage Account' seen in the navigation bar at the top. there will be an option on the right to delete your account";
                break;
            default:
                response = '';
            }
            
        $('#faq-response').text(response);
    });
>>>>>>> b6a0ca6b3bfd681a73eab6c466400890f1577bdd
});