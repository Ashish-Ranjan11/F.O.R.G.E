import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import gsap from "gsap";

import {
    FaShieldAlt,
    FaChartBar,
    FaFingerprint,
    FaSatelliteDish,
    FaBrain,
    FaNetworkWired,
    FaBolt
} from "react-icons/fa";

import forgeVideo from "../assets/videos/forge-intelligence-core.mp4";

export default function ForgeHero({

    beginInvestigation,
    openAnalytics

}){

    const hero=useRef();
    const title=useRef();
    const subtitle=useRef();
    const actions=useRef();
    const hud=useRef();
    const video=useRef();

    useEffect(()=>{

        const tl=gsap.timeline();

        tl.from(video.current,{
            scale:1.25,
            duration:1.8,
            opacity:0,
            ease:"power4.out"
        })

        .from(title.current,{
            y:120,
            opacity:0,
            scale:1.4,
            duration:1,
            ease:"power4.out"
        },"-=1")

        .from(subtitle.current,{
            y:40,
            opacity:0,
            duration:.8
        },"-=.6")

        .from(actions.current,{
            y:60,
            opacity:0,
            duration:.8
        },"-=.4")

        .from(hud.current,{
            opacity:0,
            scale:.9,
            duration:.7
        },"-=.4");

    },[]);

    return(

<section
ref={hero}
className="forge-hero">

<div className="video-wrapper">

<video

ref={video}
autoPlay
muted
loop
playsInline

className="forge-video"

>

<source
src={forgeVideo}
type="video/mp4"
/>

</video>

<div className="video-overlay"/>

<div className="video-grid"/>

<div className="video-vignette"/>

<div className="video-scan"/>

<div className="forge-content">

<div
ref={title}
className="forge-title">

F.O.R.G.E.

</div>

<div
ref={subtitle}
className="forge-subtitle">

Forensic Observation &
Recognition Gateway

<p>

Deepfake Threat Intelligence Platform

</p>

</div>

<div
ref={actions}
className="forge-buttons">

<motion.button

whileHover={{
scale:1.05
}}

whileTap={{
scale:.95
}}

onClick={beginInvestigation}

className="forge-btn-primary"

>

<FaBolt/>

Begin Investigation

</motion.button>

<motion.button

whileHover={{
scale:1.05
}}

whileTap={{
scale:.95
}}

onClick={openAnalytics}

className="forge-btn-secondary"

>

<FaChartBar/>

Open Analytics

</motion.button>

</div>

</div>

<div
ref={hud}
className="hud-layer">

<div className="hud-box left top">

<FaFingerprint/>

FACIAL MATRIX

</div>

<div className="hud-box right top">

<FaBrain/>

AI ENGINE

</div>

<div className="hud-box left bottom">

<FaSatelliteDish/>

SIGNAL

</div>

<div className="hud-box right bottom">

<FaNetworkWired/>

MULTIMODAL

</div>

</div>

</div>

</section>

)

}