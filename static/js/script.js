window.onload = function() {
    fetch('/databases')
        .then(response => response.json())
        .then(data => {
            const databasesDiv = document.getElementById('databases');
            const ul = document.createElement('ul');

            data.forEach(database => {
                const li = document.createElement('li');
                li.textContent = database;
                ul.appendChild(li);
            });

            databasesDiv.appendChild(ul);
        })
        .catch(error => console.error('Error:', error));
};
