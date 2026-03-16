import React, {useState, useEffect} from 'react'

function App() {

  const [data, setData] = useState([]);
  const [link, setLink] = useState('');
  const [loading, setLoading] = useState("Wait for submit");

  useEffect(() => {
    if(data.length != 0){
      console.log("data", data[0].message);
      setLoading("Completed")
    }
  }, [data]);

  const checkYouTubeUrl = (url) => {
    const youtubeRegex = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/gm;
    return youtubeRegex.test(url);
  };

  const downloadVideo = async() => {
    fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(link),
    })
    .then(
      response =>
        response.json()
    )
    .then(data => {
      console.log('Success:', data[0].message);
      setData(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  const onClickSubmit = async () =>{
    if(link !== ""){
      if(checkYouTubeUrl(link)){
        console.log("Link detected!");
        setLoading("Pending...")
        await downloadVideo();
        
      }else{
        console.log("Link not verified!");
      }
    }
  }

  useEffect(() =>{
    if(loading){
      console.log(loading);
    }
  },[loading])

  return (
    <div className='flex flex-col justify-center w-full'>
      <div className='flex justify-center w-full p-5 font-bold text-[25px] bg-metal rounded'>Human Action Recognition</div>
      <div className='font-bold pt-5 px-10'>
        System perform prediction based
      </div>
      <div className='flex flex-row pt-5 justify-center items-center'>
        <div className='flex'>
           Enter Youtube video link: 
        </div>
        <input className='flex ms-10 border w-[500px] ps-2' value={link} onChange={e=> setLink(e.target.value)}/>
        <button className='border ms-5 rounded p-1 hover:bg-silver active:bg-purple' 
        onClick={
          onClickSubmit
        }>
          Submit
        </button>
      </div>
      <div className='flex pt-5 justify-center items-center'>
        Status: {loading}
      </div>
      {
        data.length != 0 && <div className='flex flex-col justify-center items-center border mt-5'>

            <div className='flex font-bold'> Video title: {data[0].message}</div>
            <div className='flex'> Prediction Action: {data[1].label_predicted}</div>
            <div className='flex'> Confidence: {data[1].confidence}</div>
           </div>
      }
    </div>
  )
}

export default App