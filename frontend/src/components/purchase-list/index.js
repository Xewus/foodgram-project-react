import styles from './styles.module.css'
import cn from 'classnames'
import { Purchase } from '../index'

const PurchaseList = ({ orders = [], updateOrders, handleRemoveFromCart }) => {
  return <ul className={styles.purchaseList}>
    {orders.map(order => <Purchase
      updateOrders={updateOrders}
      handleRemoveFromCart={handleRemoveFromCart}
      key={order.id}
      {...order}
    />)}
  </ul>
}

export default PurchaseList
