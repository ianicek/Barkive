import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Dashboard.css"; // Import CSS for styling

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [pets, setPets] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (!storedUser) {
            navigate("/");
        } else {
            const userData = JSON.parse(storedUser);
            setUser(userData);
            fetchPets(userData.id);
        }
    }, [navigate]);

    const fetchPets = async (userId) => {
        try {
            const response = await axios.get(`http://localhost:5000/pets?userId=${userId}`);
            setPets(response.data);
        } catch (error) {
            console.error("Error fetching pets:", error);
        }
    };

    if (!user) return <p>Loading...</p>;

    return (
        <div className="dashboard">
            <div className="menu">
                <div className="logo">
                    <img src="barkive2.png" alt="Barkive Logo" />
                </div>
                <ul>
                    <li><a href="/dashboard">Dashboard</a></li>
                    <li><a href="/medical">Medical</a></li>
                    <li><a href="/new-owner">New Owner</a></li>
                    <li><a href="/profile">Profile</a></li>
                    <li><a href="/" onClick={() => localStorage.removeItem("user")}>Sign Out</a></li>
                </ul>
            </div>
            
            <div className="content">
                <div className="profile-box">
                    <h2>{user.username} Information</h2>
                    <p><strong>Name:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Phone:</strong> {user.phone || "N/A"}</p>
                    <a href="/profile">Edit Profile</a>
                </div>

                {pets.length > 0 ? (
                    pets.map((pet) => (
                        <div className="pet-box" key={pet.id}>
                            <h2>{pet.name} Information</h2>
                            <p><strong>Pet Name:</strong> {pet.name}</p>
                            <p><strong>Medication:</strong> {pet.medication || "N/A"}</p>
                            <p><strong>Appointment:</strong> {pet.appointment || "N/A"}</p>
                            <p><a href={`/edit-pet/${pet.id}`}>Edit Pet</a> / <a href="/add-pet">Add Pet</a></p>
                        </div>
                    ))
                ) : (
                    <p>No pets found.</p>
                )}

                <div className="image-slider">
                    <img src="dog4.jpg" alt="Dog 1" className="slide" />
                    <img src="dog2.webp" alt="Dog 2" className="slide" />
                    <img src="dog3.jpg" alt="Dog 3" className="slide" />
                </div>

                <div className="about-box">
                    <h2>About Barkive</h2>
                    <p>
                        Barkive is a comprehensive pet management system designed to help pet owners keep track of medical records, contact veterinarians, and manage essential pet care details all in one place.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
