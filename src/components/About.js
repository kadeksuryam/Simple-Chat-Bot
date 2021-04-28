import React from 'react'
import suryaImg from './assets/surya-img.jpg'
import zaidanImg from './assets/zaidan-img.png'
import akeylaImg from './assets/akeyla.jpg'
import './About.css'
const About = () => {
    return(
        <>
            <div className="about-container">
                <div className='title'>Developers</div>
                <div className='dev-container'>
                    <div className='person'>
                        <img src={suryaImg} className="pfp" alt='dev-pfp'/>
                        <div className="dev-info">Kadek Surya Mahardika</div>
                    </div>
                    <div className='person'>
                        <img src={zaidanImg} className="pfp" alt='dev-pfp'/>
                        <div className="dev-info">Zaidan Naufal Sudrajat</div>
                    </div>
                    <div className='person'>
                        <img src={akeylaImg} className="pfp" alt='dev-pfp'/>
                        <div className="dev-info">Akeyla Pradia Naufal</div>
                    </div>
                </div>
                <div className='title'>Build With</div>
                <div className='info-tech'>
                    <ul>
                        <li>ReactJS</li>
                        <li>Flask</li>
                        <li>Bootstrap</li>
                        <li>Kendo React UI</li>
                    </ul>
                </div>
            </div>
        </>
    )
}

export default About