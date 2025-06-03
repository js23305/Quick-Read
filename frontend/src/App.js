import React from 'react';
import UploadForm from './components/UploadForm';
// import ParticleBackground from './components/ParticleBackground'; // Removed animated background
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div className="App" style={{ position: 'relative', minHeight: '100vh', overflow: 'hidden' }}>
      {/* <ParticleBackground /> */}
      {/* Remove the big white box/header, keep only a slim navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark shadow-sm p-0" style={{minHeight: '56px', backgroundColor: '#0a1931'}}>
        {/* <div className="container p-0 m-0" style={{maxWidth: '100vw'}}> */}
          <a className="navbar-brand mx-auto fw-bold" href="/" style={{fontSize: '1.6rem', letterSpacing: '1px', padding: 0, margin: 0}}></a>
        {/* </div> */}
      </nav>
      <UploadForm />
      <footer className="container">
        <footer className="py-3 my-4">
          <ul className="nav justify-content-center border-bottom "></ul>
          <p className="text-center text-body-secondary">© 2025 Book Summarizer, Inc</p>
        </footer>
      </footer>
    </div>
  );
}

export default App;