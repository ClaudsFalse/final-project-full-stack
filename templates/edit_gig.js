function editGig() {
    console.log('editGig function called');
    const gigId = "{{gig_data['id']}}"
    const place = document.getElementById('place').value;
    const startTime = document.getElementById('start-time').value;
    const hourlyRate = document.getElementById('hourly-rate').value;
    const duration = document.getElementById('duration').value;
    const data = {
                id:gigId,
                place: place,
                start_time: startTime,
                hourly_rate: hourlyRate,
                duration: duration
            };
    console.log(data)
           
    fetch('/gigs/' + gigId + '/edit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }
           
        
    document.getElementById('edit-gig-form').addEventListener('submit', function(event) {
                console.log('edit-gig-form submitted');
                event.preventDefault();
                editGig();
            });