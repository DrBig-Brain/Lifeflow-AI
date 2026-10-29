import {useState} from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

export default function AuthPage({onLogin}){
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if(!username.trim() || !password.trim()) return ;
        setLoading(true);
        setError(null);

        try{
            if(!isLogin){
                await axios.post(`${API}/auth/register`, {username, email, password});
            }
            const response = await axios.post(`${API}/auth/login`, {username,password});
            console.log("response:", response.data);
            onLogin(response.data.access_token, response.data.username);
        }catch (err){
          console.log("error:", err);
            setError(err.response?.data?.detail || "something went wrong");
        }finally{
            setLoading(false);
        }
    };

    return(
        <div className="min-h-screen bg-gray-950 text-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-md">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-indigo-400">LifeFlow AI</h1>
          <p className="text-gray-400 mt-2">Multi-agent decision support system</p>
        </div>

        {/* Card */}
        <div className="bg-gray-900 rounded-2xl p-8 space-y-4">
          <h2 className="text-xl font-semibold text-center">
            {isLogin ? "Welcome back" : "Create an account"}
          </h2>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Username</label>
            <input
              className="w-full bg-gray-800 rounded-xl p-3 text-gray-100 outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="e.g. bhondu"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm text-gray-400 mb-1">Email</label>
              <input
                className="w-full bg-gray-800 rounded-xl p-3 text-gray-100 outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="e.g. bhondu@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          )}

          <div>
            <label className="block text-sm text-gray-400 mb-1">Password</label>
            <input
              type="password"
              className="w-full bg-gray-800 rounded-xl p-3 text-gray-100 outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && <p className="text-red-400 text-sm text-center">{error}</p>}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-900 disabled:text-indigo-400 text-white font-semibold py-3 rounded-xl transition-all"
          >
            {loading ? "Please wait..." : isLogin ? "Login →" : "Register →"}
          </button>

          <p className="text-center text-sm text-gray-400">
            {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
            <button
              onClick={() => { setIsLogin(!isLogin); setError(null); }}
              className="text-indigo-400 hover:text-indigo-300 font-medium"
            >
              {isLogin ? "Register" : "Login"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
