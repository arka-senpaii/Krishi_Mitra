# Krishi Mitra – कृषि मित्र 🌱

A beautiful and responsive smart agriculture landing page built with modern web technologies. This project demonstrates real-time sensor data monitoring for smart farming solutions.

## 🚀 Features

- **Responsive Design**: Works perfectly on mobile, tablet, and desktop devices
- **3D Animations**: Beautiful Three.js background animations with floating agricultural particles
- **Smooth Animations**: Anime.js powered scroll and interaction animations
- **Real-time Data**: Firebase Realtime Database integration for live sensor monitoring
- **Modern UI**: Clean, agricultural-themed design with green, yellow, and brown color palette
- **Sensor Monitoring**: 
  - DHT22 Temperature & Humidity sensor
  - Rain detection sensor
  - Soil moisture monitoring
  - Real-time Firebase updates

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Animations**: Anime.js for smooth transitions and interactions
- **3D Graphics**: Three.js for background particle system
- **Database**: Firebase Realtime Database (read-only integration)
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome icons
- **Fonts**: Google Fonts (Poppins)

## 📁 Project Structure

```
krishi-mitra/
├── index.html          # Main HTML file
├── style.css           # Main stylesheet
├── main.js             # Main JavaScript logic
├── firebase.js         # Firebase configuration and data handling
├── assets/             # Images and icons directory
└── README.md           # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Modern web browser with JavaScript enabled
- Node.js and npm (for development dependencies)
- Firebase project (optional - falls back to mock data)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd krishi-mitra
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure Firebase (Optional)**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Realtime Database
   - Copy your Firebase configuration
   - Update `firebase.js` with your config:

   ```javascript
   const firebaseConfig = {
       apiKey: "your-api-key",
       authDomain: "your-project.firebaseapp.com",
       databaseURL: "https://your-project-default-rtdb.firebaseio.com/",
       projectId: "your-project-id",
       storageBucket: "your-project.appspot.com",
       messagingSenderId: "123456789",
       appId: "your-app-id"
   };
   ```

4. **Set up Firebase data structure**
   ```json
   {
     "sensorData": {
       "temperature": 28.5,
       "humidity": 65,
       "soilMoisture": 45,
       "rainfall": 0,
       "timestamp": "2025-01-08T10:30:00.000Z"
     }
   }
   ```

5. **Run the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser** and navigate to the local server URL

## 🎯 Usage

### Navigation
- Use the navigation bar to jump to different sections
- Mobile-responsive hamburger menu for smaller screens
- Smooth scroll animations between sections

### Live Data Monitoring
- Sensor data updates automatically every 5 seconds
- Color-coded status indicators (Normal/Warning/Danger)
- Real-time timestamp updates
- Fallback to mock data when Firebase is not configured

### 3D Background Animation
- Interactive particle system representing agricultural elements
- Responsive to screen size changes
- Optimized performance with animation pausing when tab is inactive

## 🎨 Customization

### Colors
The CSS uses custom properties for easy theming:

```css
:root {
    --primary-green: #2d6a2f;
    --secondary-green: #4caf50;
    --accent-yellow: #ffc107;
    --soil-brown: #8d4925;
    /* ... more colors */
}
```

### Animation Settings
Modify animation parameters in `main.js`:

```javascript
// Example: Change hero title animation
anime({
    targets: '.hero-title',
    translateY: [50, 0],
    opacity: [0, 1],
    duration: 1000,    // Adjust duration
    easing: 'easeOutQuart',
    delay: 600         // Adjust delay
});
```

### Sensor Data
Add more sensors by:
1. Updating the Firebase data structure
2. Adding new cards in the HTML
3. Extending the `updateSensorDisplay()` function

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: > 1024px

## 🔧 Development

### Adding New Features

1. **New Sensor Type**:
   - Add HTML card in the live data section
   - Update CSS for styling
   - Extend JavaScript data handling

2. **Additional Animations**:
   - Use Anime.js for new elements
   - Add intersection observers for scroll triggers
   - Maintain performance with proper cleanup

3. **Enhanced 3D Effects**:
   - Modify Three.js particle system
   - Add new geometries or materials
   - Implement user interactions

### Performance Optimization

- Animations pause when page is not visible
- Three.js renderer optimization
- Efficient Firebase listeners
- Responsive image loading

## 🌐 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🆘 Troubleshooting

### Firebase Connection Issues
- Check your Firebase configuration
- Verify database rules allow read access
- Ensure network connectivity
- Check browser console for error messages

### Animation Performance
- Reduce particle count in Three.js scene
- Adjust animation durations
- Check device performance capabilities

### Mobile Display Issues
- Test on actual devices
- Verify viewport meta tag
- Check CSS media queries

## 📞 Support

For questions or issues:
- Email: krishimitra@example.com
- GitHub: [Repository Issues](https://github.com/your-repo/issues)

---

**Made with ❤️ by Team Krishi Mitra**

*Empowering farmers with technology for a sustainable future* 🌾