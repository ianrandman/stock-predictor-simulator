export default class Network{
  static  getData = (stock, successCallback, failCallback)=>{
    window.fetch(`https://df47b474-1a33-43be-95bf-c1510c2740ee.mock.pstmn.io/data?stock=${stock}`).then((resp)=>{
      if(resp.ok){
        resp.text().then((json)=>{
          successCallback(json);
        });
      }else{
        resp.text().then((json)=>{
          failCallback(json);
        });
      }
    })
  };

  static predict = (stock, date, successCallback, failCallback)=>{
    window.fetch(`https://df47b474-1a33-43be-95bf-c1510c2740ee.mock.pstmn.io/predict?stock=${stock}&date=${date}`).then((resp)=>{
      if(resp.ok){
        resp.text().then((json)=>{
          successCallback(json);
        });
      }else{
        resp.text().then((json)=>{
          failCallback(json);
        });
      }
    })
  }
}