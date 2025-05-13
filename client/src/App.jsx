import { useState } from 'react'
import {RouterProvider} from "react-router-dom";
import './App.css'
import { router } from './app/routes/router';

function App() {

  return (
    <div>
      <RouterProvider router={router}/>
    </div>
  )
}

export default App
