import React from 'react';
import './FileUpload.css'

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      body: '',
    };

    this.processFile = this.processFile.bind(this);
    this.saveToDb = this.saveToDb.bind(this);
  }

  processFile(ev) {
    ev.preventDefault();
    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    
    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((result) => {
        this.setState({ body: result });
        this.setState({filename: this.uploadInput.files[0].name})
      });
    });
  }


  financial(x) {
    if (x)
      return Number.parseFloat(x).toFixed(2);
  }

  saveToDb(ev) {
    ev.preventDefault()

    const data = this.state.body
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    };
    fetch('http://localhost:5000/save', requestOptions)
    .then((response) => {
      response.json().then((result) => {
        alert('Invoice inserted.')
      });
    });
}



  render() {
    return (
      <div class="form-style-2">
        <div class="form-style-2-heading">Typless Invoice classifier</div>
        <form onSubmit={this.saveToDb}>
          <div>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file"/>
            <br />
            <br />
            <button onClick={ this.processFile }>Process</button>
            <br />
            
          </div>
          <div>
            
          <label for="supplier_name"><span>Supplier name</span><input type="text" id="supplier_name" value= {this.state.body.supplier_name} class="input-field"/></label>
          <label for="invoice_number"><span>Invoice Number: </span><input type="text" id="invoice_number" value={this.state.body.invoice_number} class="input-field"/></label>
          <label for="issue_date"><span>Issue date: </span><input type="text" id="issue_date" value={this.state.body.issue_date} class="input-field"/></label>
          <label for="pay_due_date"><span>Due date: </span> <input type="text" id="pay_due_date" value= {this.state.body.pay_due_date} class="input-field"/></label>
          <label for="total_amount"><span>Total: </span>  <input type="text" id="total_amount" value= {this.financial(this.state.body.total_amount)} class="input-field"/></label>
          </div>
          <div>
          <input type="submit" value="Save"></input>
          </div>
          
        </form>
      </div>
    );
  }
}

export default Main;
