import React, { useState, useEffect} from 'react'

function App() {

  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/members").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])
  return (
    <div className='container-fluid'>
      {(typeof data.artist === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        <React.Fragment>
          <div className='row justify-content-md-center mt-3'>
            <div className='card' style={{width:'18rem'}}>
              <img className="card-img-top" src={data.artist.image_url} alt={data.artist.name}></img>
              <div className="card-body">
                <p className="card-text" style={{textAlign:'center'}}>{data.artist.name}</p>
              </div>
            </div>
            </div>
            <div className='row justify-content-md-center mt-3'>
              {data.artist.albums.map((album) => (
                <div key={album.id} className='card' style={{width:'18rem'}}>
                  <img className="card-img-top" src={album.image_url} alt={album.name}></img>
                  <div className="card-body">
                    <a href={'/album/'+album.id} className="stretched-link">
                      <p className="card-text" style={{textAlign:'center'}}>{album.name}</p>
                    </a>
                  </div>
                </div>
              ))}  
            </div>
        </React.Fragment>
      )}
      {/*
      {(typeof data.artist.albums === 'undefined') ? (
          <p>Loading...</p>
        ) : (
          {
            data.artist.albums.map(album => (
              <React.Fragment>
                <div className='card' style={{width:'18rem'}}></div>
                <img className="card-img-top" src={data.artist.image_url} alt={data.artist.name}></img>
                <div className="card-body">
                  <p className="card-text" style={{textAlign:'center'}}>{data.artist.name}</p>
                  <button type="button" className="btn btn-dark stretched-link btn-block" onClick={showAlbums}>Get Albums</button>
                </div>
              </React.Fragment>
            ))
          }
        )}*/}
    </div>
  )
}

export default App