import React, { useEffect, useState } from "react"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";


export const Profile = () => {

    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    const [usuario, setUser] = useState({}); 

    const getData = async () => {
        const resp = await fetch(`https://silver-trout-v6rx6x944wv536xgr-3001.app.github.dev/api/user`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        }
    });

    const data = await resp.json()
    setUser({
          name: data.user.name,
          email: data.user.email,
        });

    }

    useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
        alert("Inicia sesion antes de continuar")
      navigate('/login');
      return;
    }
    getData()
  }, []);


    const onLogout = () => {
        localStorage.removeItem('token');
        navigate("/login")
    }

    return (
        <div className="container mt-5">
            <div className="card mx-auto">
                <div className="card-body text-center">
                    <img
                        src="https://cdn-icons-png.freepik.com/512/16/16480.png"
                        alt="Foto de perfil"
                        className="rounded-circle mb-3"
                        width="120"
                        height="120"
                    />
                    <h4 className="card-title">{usuario.name}</h4>
                    <p className="card-text text-muted">{usuario.email}</p>
                    
                    <button className="btn btn-danger mt-3" onClick={onLogout}>
                        Cerrar sesión
                    </button>
                </div>
            </div>
        </div>
    );
};