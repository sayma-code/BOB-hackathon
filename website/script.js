// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Animated counter for debt value
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        obj.textContent = current.toFixed(1);
    }, 16);
}

// Start animation when page loads
window.addEventListener('load', () => {
    animateValue('debt-value', 0, 96.5, 2000);
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all solution cards
document.querySelectorAll('.solution-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(card);
});

// Observe timeline items
document.querySelectorAll('.timeline-item').forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateX(-30px)';
    item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(item);
});

// Observe requirement cards
document.querySelectorAll('.requirement-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'scale(0.9)';
    card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(card);
});

// Add active class to navigation on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLink?.classList.add('active');
        } else {
            navLink?.classList.remove('active');
        }
    });
});

// Add hover effect data to cards
document.querySelectorAll('.solution-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.borderColor = 'var(--primary-color)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.borderColor = 'var(--border-color)';
    });
});

// Mobile menu toggle (if needed in future)
const createMobileMenu = () => {
    const nav = document.querySelector('.nav-links');
    const menuBtn = document.createElement('button');
    menuBtn.className = 'mobile-menu-btn';
    menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
    menuBtn.style.display = 'none';
    
    if (window.innerWidth <= 768) {
        menuBtn.style.display = 'block';
        document.querySelector('.navbar .container').appendChild(menuBtn);
        
        menuBtn.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }
};

// Initialize on load
window.addEventListener('load', createMobileMenu);
window.addEventListener('resize', createMobileMenu);

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s';
        document.body.style.opacity = '1';
    }, 100);
});

// Console message
console.log('%cBangladesh Economic Transformation', 'color: #2563eb; font-size: 20px; font-weight: bold;');
console.log('%cA comprehensive strategy for debt reduction and economic growth', 'color: #10b981; font-size: 14px;');
console.log('%c$62.6B Annual Revenue Potential | 10.8x ROI | 10M+ Jobs', 'color: #f59e0b; font-size: 12px;');

// Made with Bob
