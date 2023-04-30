/* Responsible for navigating to the correct component based on the path
we are currently at      */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ChatBox from './components/ChatBox'
import ArcGISMap from './components/leaflet';
import SignUp from './components/SignUp';
import Splash from './components/Splash';
import "./style.css"

function App() {
  return (
    <BrowserRouter>
      {/* Route Components */}
      <Routes>
        <Route path="/" element={<Splash/>}/>
        <Route path="/signup" element={<SignUp/>}/>
        <Route path="/chat" element={<ChatBox/>}/>
        <Route path="/map" element={<ArcGISMap/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
