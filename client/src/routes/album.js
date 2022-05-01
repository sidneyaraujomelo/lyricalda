import React, { useState, useEffect} from "react"
import {Link, useParams} from 'react-router-dom'

function Album(){
    let params = useParams();
    const [data, setData] = useState([{}])
    useEffect(() => {
        fetch("/album/"+params.albumId).then(
        res => res.json()
        ).then(
        data => {
            setData(data)
            console.log(data)
        }
        )
    }, [])
    return(
        <div className='container-fluid'>
        {(typeof data.album_cover === 'undefined') ? (
            <p>Loading...</p>
        ) : (
            <React.Fragment>
                <div className="row align-items-start justify-content-start">
                    <div className="col-4">
                        <div className="row">
                            <div className="col-6">
                                <img src={data.album_cover} alt={data.album_name} className='img-thumbnail'></img>
                            </div>
                            <div className="col-6">
                                <div className="row  align-self-center">
                                    <h5>{data.album_name}</h5>
                                    <Link to="/">
                                        <p>{data.album_artist}</p>
                                    </Link>
                                </div>
                            </div>
                        </div>
                        <ul className="list-group">
                        {data.songs.map((song) =>
                            <li key={song.id} className="list-group-item">{song.title}</li>
                        )}
                        </ul>
                    </div>
                    <div className="col-8">
                            <div className="row align-self-center">
                                <div className="accordion" id={"accordion_"+data.album_id}>
                                    {data.topics.map((topic, i) =>
                                        <div className="accordion-item" key={i}>
                                            <h2 className="accordion-header" id={'id_topic_'+i}>
                                                <button className="accordion-button collapsed" type='button' 
                                                data-bs-toggle="collapse" data-bs-target={'#collapse_'+i}
                                                aria-expanded="false" aria-controls={'collapse_'+i}>
                                                    {'Topic '+(i+1)+': '+topic.words.join(", ")}
                                                </button>
                                            </h2>
                                            <div id={"collapse_"+i} className="accordion-collapse collapse"
                                            aria-labelledby={'id_topic_'+i} data-bs-parent={"accordion_"+data.album_id}>
                                                <div className="accordion-body">
                                                    <p>{'Most related songs: '+topic.songs.join(", ")}</p>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                    </div>
                </div>
            </React.Fragment>
        )}
        </div>
    )
}

export default Album