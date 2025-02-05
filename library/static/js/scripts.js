// Fetch books from the server
function fetchBooks() {
    fetch('/api/books/') // Update with your actual API endpoint
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('book-list');
            bookList.innerHTML = ''; // Clear existing books

            data.forEach(book => {
                const bookDiv = document.createElement('div');
                bookDiv.className = 'book';
                bookDiv.innerHTML = `
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                    ${book.image ? `<img src="${book.image}" alt="${book.title}" style="width: 100px; height: auto;">` : '<p>No image available</p>'}
                `;
                bookList.appendChild(bookDiv);
            });
        })
        .catch(error => console.error('Error fetching books:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!confirm('Are you sure you want to submit this form?')) {
                event.preventDefault();
            }
        });
    });
});

function toggleAuth() {
    const title = document.getElementById('auth-title');
    const form = document.getElementById('auth-form');
    const emailGroup = document.getElementById('email-group');
    const confirmPasswordGroup = document.getElementById('confirm-password-group');
    const toggleMessage = document.getElementById('toggle-message');
    const toggleLink = document.getElementById('toggle-link');

    if (title.textContent === 'Login') {
        // Switch to Sign Up
        title.textContent = 'Sign Up';
        emailGroup.style.display = 'block';
        confirmPasswordGroup.style.display = 'block';
        toggleMessage.innerHTML = 'Already have an account? <a href="#" id="toggle-link" onclick="toggleAuth()">Login here</a>.';
        form.action = '/signup/'; // Update form action for signup
    } else {
        // Switch to Login
        title.textContent = 'Login';
        emailGroup.style.display = 'none';
        confirmPasswordGroup.style.display = 'none';
        toggleMessage.innerHTML = "Don't have an account? <a href='#' id='toggle-link' onclick='toggleAuth()'>Sign up here</a>.";
        form.action = '/login/'; // Update form action for login
    }
}


// Function to get CSRF token from the cookie
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = cookie.substring(10);
                break;
            }
        }
    }
    return cookieValue;
}
// Function to handle POST requests for add-to-cart, wishlist, and delete actions
function handlePostRequest(element, confirmAction = false) {
    if (confirmAction && !confirm('Are you sure you want to delete this book?')) {
        return;
    }

    const url = element.getAttribute('data-url');  // Get URL from data attribute
    const csrfToken = getCSRFToken();  // Get CSRF token

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,  // Include CSRF token in headers
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            location.reload(); // Reload the page to reflect changes
        } else {
            alert('Something went wrong!');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong!');
    });
}


// Function to update and display the current time
function updateTime() {
    const timeDisplay = document.getElementById("time-display");
    if (timeDisplay) {
        setInterval(() => {
            const now = new Date();
            timeDisplay.textContent = now.toLocaleTimeString();
        }, 1000);
    }
}

// Run the time update function when the script loads


document.addEventListener("DOMContentLoaded", function () {
    function updateTime() {
        const timestampElement = document.getElementById("current-time");
        if (timestampElement) {
            const now = new Date();
            const formattedTime = now.toLocaleString("en-US", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                hour12: true
            });
            timestampElement.innerText = "Added on: " + formattedTime;
        }
    }

    setInterval(updateTime, 1000); 
    updateTime(); 
});
