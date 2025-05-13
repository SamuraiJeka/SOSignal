import { createBrowserRouter } from "react-router-dom"
import LoginPage from "../../pages/LoginPage/LoginPage"
import RegistrationPage from "../../pages/RegistrationPage/RegistrationPage"
import MainPage from "../../pages/MainPage/MainPage"
export const router = createBrowserRouter(
    [
        {
            path: "/",
            element: <LoginPage/>
        },
        {
            path: "/Registration",
            element: <RegistrationPage/>
        },
        {
            path: "/MainPage",
            element: <MainPage/>
        }
    ]
)
