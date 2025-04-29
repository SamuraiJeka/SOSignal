import { createBrowserRouter } from "react-router-dom"
import LoginPage from "../../pages/LoginPage/LoginPage"
import RegistrationPage from "../../pages/RegistrationPage/RegistrationPage"
export const router = createBrowserRouter(
    [
        {
            path: "/",
            element: <LoginPage/>
        },
        {
            path: "/Registration",
            element: <RegistrationPage/>
        }
    ]
)
