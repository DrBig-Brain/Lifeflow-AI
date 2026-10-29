import {useState} from "react";
import AuthPage from "./pages/AuthPage";
import DecisionPage from "./pages/DecisionPage";

export default function App(){
    const [token,setToken] = useState(null);
    const [username, setUsername] = useState(null);

    const handleLogin = (accessToken, user) => {
        setToken(accessToken);
        setUsername(user);
    };

    const handleLogout = () => {
        setToken(null);
        setUsername(null);
    };

    if(!token){
        return <AuthPage onLogin={handleLogin}/>
    }
    return <DecisionPage token = {token} username={username} onLogout = {handleLogout}/>;
}   